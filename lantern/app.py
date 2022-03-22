import time
import json
from .color import Color
from .renderer import Renderer
from .colors import hex_colors
from .view import View
from .logging import logger
from .config_provider import ConfigProvider
from binascii import hexlify
import sys

try:
    from machine import unique_id
    from machine import Pin
    from machine import ADC
    from machine import reset
    from machine import deepsleep
    from network import WLAN
    from time import ticks_ms
    from .mqtt import MQTTClient
    from umqtt.simple import MQTTException
    from gc import mem_free
except (ImportError, ModuleNotFoundError) as e:
    from mocks import unique_id
    from mocks import Broker as MQTTClient    
    from mocks import Pin 
    from mocks import ADC   
    from mocks import WLAN
    from mocks import reset
    from mocks import deepsleep
    from mocks import ticks_ms
    from mocks import MQTTException
    from mocks import mem_free

class App():
    def __init__(self, updater, id=None):
        
        self.provider = ConfigProvider()
        self.updater = updater

        runtime = self.provider.config['runtime']
        config = self.provider.config['network']

        if runtime['DEBUG']:
            logger.enable()

        if id is None:
            self.id = hexlify(unique_id()).decode()
        else:
            self.id = id

        self.broker = MQTTClient(self.id, config['mqtt_server'], config['mqtt_port'], config['mqtt_user'], config['mqtt_password'])
        self.broker.DEBUG = True
        self.broker.set_callback(self.subscription_callback)


        self.view = View(Pin(runtime['VIEW_PIN'], Pin.OUT) , runtime['NUMBER_OF_PIXELS'])    
        self.renderer = Renderer(self.view, runtime['RENDER_INTERVAL'])

        self.version = ""
        self.paused = False   

    def subscription_callback(self, topic, message):
        logger.log(topic.decode('utf-8'))
        topic = topic.decode("utf-8")
        self.paused = False
        self.last_update = ticks_ms()
        s = topic.split("/")

        if "color" in topic:
            logger.log("Color update")
            data = json.loads(message)
            self.renderer.update_animation(data)
            self.ping()
        
        elif "sync" in topic:
            logger.log("sync request")
            pass
        
        elif "poke" in topic:
            logger.log("Poke request")
            self.connect()
        
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
                self.provider.update_runtime_config(message)
        
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


    def ping(self):
        update = json.dumps({
            "id" : self.id,
            "color" : self.renderer.current_color.as_hex(),
            "memory": mem_free()
            })
        self.broker.publish("ping", update)

    def connect(self):
        update = json.dumps({
            "id" : self.id,
            "color" : self.renderer.current_color.as_hex(),
            "version": self.version,
            "platform": sys.platform,
            "config": self.provider.config['runtime']
            })
        self.broker.publish("connect", update)

    def set_version(self):
        try:
            f = open("lantern/.version", "r")
            self.version = f.read()
            f.close()
        except OSError:
            self.version = "dev"

    def backup(self):
        logger.log("starting backup sequence")
        color_int = 0
        self.last_update = ticks_ms()
        self.backup_started = ticks_ms()
        config = self.provider.config['runtime']
        while ticks_ms() < self.backup_started + config['BACKUP_INTERVAL']:
            current_time = ticks_ms()
            if (self.last_update + 5000 < current_time):
                hex = hex_colors[color_int]
                color = Color(0,0,0)
                color.from_hex(hex)
                data = {
                    "color": color.as_hex(),
                    "time": 2000
                }
                self.update_animation(data)
                self.last_update = current_time
                color_int = color_int + 1
                if(color_int >= len(hex_colors)):
                    color_int = 0

            self.renderer.check_and_render(current_time, config['RENDER_INTERVAL'])
        logger.log("Restarting")
        self.view.off()
        reset()

    def subscribe(self):
        logger.log("Subscribing")
        self.broker.subscribe("sync")
        self.broker.subscribe("poke")
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
            logger.log('connecting to network...')
            wlan.connect(config['ssid'], config['password'])
            while not wlan.isconnected():    
                time.sleep(1.0)
                pass

        logger.log(wlan.ifconfig()) 
        time.sleep(1.0)


    def main(self):

        try:
            config = self.provider.config['network']
            runtime = self.provider.config['runtime']

            self.updater.download_and_install_update_if_available(config['ssid'], config['password'])
            logger.log("Starting app")
        
            self.set_version()
            self.connect_to_wifi(config)
            self.broker.connect()
            self.subscribe()
            self.connect()
            
            self.view.off()
            self.last_update = ticks_ms()

            sleep_interval = runtime['SLEEP_INTERVAL']
            

            while True:
                current_time = ticks_ms()

                if ((self.last_update + sleep_interval < current_time) and not self.paused):
                    self.paused = True
                    self.renderer.update(Color(0,0,0), current_time, 1000, "ElasticEaseOut")
                    self.last_update = current_time
                    self.ping()
                else:
                    self.renderer.check_and_render(current_time)

                self.broker.check_msg()
                    
        except (TypeError, OSError, Exception, MQTTException) as e:
            logger.warn(e)
            self.backup()
        except(KeyboardInterrupt) as e:
            self.view.off()
            logger.log("Exiting")
            pass