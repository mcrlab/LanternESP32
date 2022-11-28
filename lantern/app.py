import time
import json
from .color import HexColor, to_hex
from .view import View
from .logging import logger
from .config_provider import provider
from binascii import hexlify
from .ota_updater import OTAUpdater
import sys

try:
    from machine import unique_id
    from machine import Pin
    from machine import reset
    from machine import deepsleep
    from network import WLAN
    from time import ticks_ms
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
    from mocks import ticks_ms

RED = HexColor("FF0000")
GREEN = HexColor("00FF00")
BLUE = HexColor("0000FF")
BLACK = HexColor("000000")

class App():
    def __init__(self, udpater=None, id=None):
        
        config = provider.config

        self.updater = OTAUpdater('https://github.com/mcrlab/LanternESP32', module='./', main_dir='lantern', proxy=config['PROXY_SERVER'])

        self.sleep_interval = config['SLEEP_INTERVAL']

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
        self.last_update = 0
        
        
    def subscription_callback(self, topic, message):
        self.last_update = ticks_ms()
        if(type(topic) is bytes):
            topic = topic.decode("utf-8")
        logger.log(topic)

        s = topic.split("/")

        if "color" in topic:
            logger.log("Color update")
            logger.log(message)
            self.view.render_color(HexColor(message))
        
        elif "poke" in topic:
            logger.log("Poke request")
            self.call_home()
        
        elif "update" in topic:
            if len(s) == 1 or (len(s) > 1 and s[1] == self.id):
                logger.log("Firmware Update")
                self.view.off()  
                self.broker.disconnect()
                self.view.render_color(BLUE)
                self.updater.check_for_update_to_install_during_next_reboot()
                self.flash(BLUE)
                reset()
        
        elif "config" in topic:
            if len(s) == 1 or (len(s) > 1 and s[1] == self.id):
                logger.log("config update")
                self.view.render_color(GREEN)
                provider.update_config(message)
                self.flash(GREEN)
                reset()
        
        elif "sleep" in topic:
            if len(s) == 1 or (len(s) > 1 and s[1] == self.id):
                logger.log("sleeping")
                self.view.off()  
                data = json.loads(message)
                deepsleep(data["seconds"] * 1000)

        elif "restart" in topic:
            if len(s) == 1 or (len(s) > 1 and s[1] == self.id):
                self.flash(RED)
                logger.log("restarting")
                reset()
        else:
            logger.log("unknown command")

    def register(self):
        update = json.dumps({
            "id" : self.id,
            "color" : to_hex(self.view.current_color),
            "version": self.version,
            "platform": sys.platform,
            "config": provider.config
            })
        logger.log("Registering Light")
        self.broker.publish("register", update)

    def flash(self, color):
        for i in range(0,3):
            self.view.render_color(color)
            time.sleep(0.25)
            self.view.off() 
            time.sleep(0.25)

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
        
        logger.log("Starting app V:{0}".format(self.version))
        logger.log("ID {0}".format(self.id))
        self.connect_to_wifi(config)
        self.updater.download_and_install_update_if_available()
        self.broker.connect()
        self.subscribe()
        self.register()
        
        while True:        
            self.view.render()
            if (self.last_update + self.sleep_interval  < ticks_ms()) and self.view.current_color is not BLACK:
                logger.log("Sleeping") 
                logger.log(self.last_update)
                logger.log(self.sleep_interval)
                logger.log(ticks_ms())
                self.view.render_color(BLACK)
            self.broker.check_msg()
    except (TypeError, OSError, Exception, MQTTException) as e:
        logger.warn(e)
        print(e)
    except(KeyboardInterrupt) as e:
        logger.log("Exiting")
        pass
    finally:
        self.view.off()
        logger.log("sleeping")
        time.sleep(10)
        reset()
