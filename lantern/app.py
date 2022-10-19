import time
import json
from .color import HexColor
from .view import View
from .logging import logger
from .config_provider import provider
from binascii import hexlify
import sys

try:
    from machine import unique_id
    from machine import Pin
    from machine import reset
    from machine import deepsleep
    from network import WLAN

    from .mqtt import MQTTClient
    from umqtt.simple import MQTTException

except (ImportError, ModuleNotFoundError) as e:
    from mocks import unique_id
    from mocks import Broker as MQTTClient    
    from mocks import Pin  
    from mocks import WLAN
    from mocks import reset
    from mocks import deepsleep
    from mocks import MQTTException

class App():
    def __init__(self, updater, id=None):
        
        self.updater = updater
       
        config = provider.config

        if config['LOGGING']:
            logger.enable()

        if id is None:
            self.id = hexlify(unique_id()).decode()
        else:
            self.id = id

        self.broker = MQTTClient(self.id, config['MQTT_SERVER'], config['MQTT_PORT'], config['MQTT_USER'], config['MQTT_PASSWORD'])
        self.broker.DEBUG = False
        self.broker.set_callback(self.subscription_callback)
        self.view = View(Pin(config['VIEW_PIN'], Pin.OUT) , config['NUMBER_OF_PIXELS'])    
        self.version = self.get_version()

    def subscription_callback(self, topic, message):
        if(type(topic) is bytes):
            topic = topic.decode("utf-8")
        logger.log(topic)
        s = topic.split("/")

        if "color" in topic:
            logger.log("Color update")
            data = json.loads(message)
            logger.log(message)
            self.view.render_color(HexColor(data['color']))
        
        elif "frame" in topic:
            if self.id in message:
                logger.log("Frame update")
                logger.log(message)
                data = json.loads(message)
                for instruction in data:
                    if instruction['address'] == self.id:            
                        self.view.render_color(HexColor(instruction['color']))
            else:
                # frame message not for us
                pass    
        
        elif "poke" in topic:
            logger.log("Poke request")
            self.call_home()
        
        elif "update" in topic:
            if len(s) == 1 or (len(s) > 1 and s[1] == self.id):
                logger.log("Firmware Update")
                self.view.off()  
                self.broker.disconnect()
                self.updater.check_for_update_to_install_during_next_reboot()
                logger.log("checked")
                reset()
        
        elif "config" in topic:
            if len(s) == 1 or (len(s) > 1 and s[1] == self.id):
                logger.log("config update")
                provider.update_config(message)
        
        elif "sleep" in topic:
            if len(s) == 1 or (len(s) > 1 and s[1] == self.id):
                logger.log("sleeping")
                self.view.off()  
                data = json.loads(message)
                deepsleep(data["seconds"] * 1000)

        elif "restart" in topic:
            if len(s) == 1 or (len(s) > 1 and s[1] == self.id):
                self.view.off() 
                logger.log("restarting")
                reset()
        else:
            logger.log("unknown command")

    def register(self):
        update = json.dumps({
            "id" : self.id,
            "color" : self.view.current_color.as_hex(),
            "version": self.version,
            "platform": sys.platform,
            "config": provider.config
            })
        logger.log("Registering Light")
        self.broker.publish("register", update)

    def get_version(self):
        try:
            f = open("lantern/.version", "r")
            data= f.read()
            f.close()
            return data
        except OSError:
            return "dev"

    def subscribe(self):
        logger.log("Subscribing to topics")
        self.broker.subscribe("color")
        self.broker.subscribe("color/"+self.id)

        self.broker.subscribe("frame")

        self.broker.subscribe("update")
        self.broker.subscribe("update/"+self.id)

        self.broker.subscribe("config")
        self.broker.subscribe("config/"+self.id)

        self.broker.subscribe("restart")
        self.broker.subscribe("restart/"+self.id)

        self.broker.subscribe("sleep")
        self.broker.subscribe("sleep/"+self.id)

    
    def connect_to_wifi(self, config):
        wlan = WLAN(0)
        wlan.active(True)
        time.sleep(1.0)
        if not wlan.isconnected():
            logger.log('Connecting to {0}'.format(config['SSID']))
            wlan.connect(config['SSID'], config['PASSWORD'])
            while not wlan.isconnected():    
                time.sleep(1.0)
                pass

        logger.log(wlan.ifconfig()) 
        time.sleep(1.0)


    def main(self):

        try:
            config = provider.config
            self.updater.download_and_install_update_if_available(config['SSID'], config['PASSWORD'])
            logger.log("Starting app V:{0}".format(self.version))
            logger.log("ID {0}".format(self.id))
            self.connect_to_wifi(config)
            self.broker.connect()
            self.subscribe()
            self.register()
            
            while True:        
                self.broker.check_msg()
                self.view.render()
                        
        except (TypeError, OSError, Exception, MQTTException) as e:
            logger.warn(e)
        except(KeyboardInterrupt) as e:
            logger.log("Exiting")
            pass
        finally:
            self.view.off()
            time.sleep(30)
            reset()
