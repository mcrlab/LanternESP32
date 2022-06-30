import time
import json
from .palette import Palette
from .animation import Animation
from .color import Color
from .color import HexColor
from .renderer import Renderer
from .colors import hex_colors
from .view import View
from .logging import logger
from .config_provider import provider
from binascii import hexlify
import sys
from .timer import get_local_time, get_server_time
from .timer import update_time_offset
from .queue import LinkedList
from math import ceil

try:
    from machine import unique_id
    from machine import Pin
    from machine import reset
    from machine import deepsleep
    from network import WLAN

    from .mqtt import MQTTClient
    from umqtt.simple import MQTTException
    from gc import mem_free
except (ImportError, ModuleNotFoundError) as e:
    from mocks import unique_id
    from mocks import Broker as MQTTClient    
    from mocks import Pin  
    from mocks import WLAN
    from mocks import reset
    from mocks import deepsleep
    from mocks import MQTTException
    from mocks import mem_free

class App():
    def __init__(self, updater, id=None):
        
        self.updater = updater
       
        config = provider.config

        if config['LOGGING']:
            logger.enable()
            self.debug_mode = True
        else:
            self.debug_mode = False

        if id is None:
            self.id = hexlify(unique_id()).decode()
        else:
            self.id = id

        self.broker = MQTTClient(self.id, config['MQTT_SERVER'], config['MQTT_PORT'], config['MQTT_USER'], config['MQTT_PASSWORD'])
        self.broker.DEBUG = True
        self.broker.set_callback(self.subscription_callback)


        self.view = View(Pin(config['VIEW_PIN'], Pin.OUT) , config['NUMBER_OF_PIXELS'])    
        self.renderer = Renderer(self.view, config['RENDER_INTERVAL'])

        self.version = ""
        self.paused = False   
        self.animation_list = LinkedList()
        self.debug_pin = Pin(15, Pin.OUT)

    def subscription_callback(self, topic, message):
        if(type(topic) is bytes):
            topic = topic.decode("utf-8")
        self.paused = False
        self.last_update = get_local_time()
        s = topic.split("/")

        if "color" in topic:
            logger.log("Color update")
            data = json.loads(message)

            local_time = get_local_time()

            target_color = HexColor(data['color'])

            palette = Palette(self.renderer.current_color, target_color)

            animation_length = data['time']

            if 'start_time' in data:
                animation_start_time = data['start_time']
            else:
                animation_start_time = local_time

            if 'easing' in data:
                easing = data['easing']
            else:
                easing = "ElasticEaseOut"

            animation = Animation(animation_start_time, animation_length, easing, palette)
            if self.animation_list.head is None:
                self.renderer.update_animation(animation)
            self.animation_list.append(animation)
        
        elif "sync" in topic:
            logger.log("sync request")
            server_time = int(message)
            update_time_offset(server_time)
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
            "config": provider.config
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
        current_time = get_local_time()
        self.last_update = current_time
        self.backup_started = current_time
        config = provider.config
        while current_time < self.backup_started + config['BACKUP_INTERVAL']:
            current_time = get_local_time()
            if (self.last_update + 5000 < current_time):
                hex = hex_colors[color_int]
                target_color = HexColor(hex)

                palette = Palette(self.renderer.current_color, target_color)

                animation_length = 1000
                animation_start_time = current_time
                easing = "ElasticEaseOut"

                animation = Animation(animation_start_time, animation_length, easing, palette)

                self.renderer.update_animation(animation)

                self.last_update = current_time
                color_int = color_int + 1
                if(color_int >= len(hex_colors)):
                    color_int = 0

            self.renderer.render(current_time)

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
            logger.log("Starting app")
            logger.log("ID {0}".format(self.id))
            self.set_version()
            self.connect_to_wifi(config)
            self.broker.connect()
            self.subscribe()
            self.connect()
            
           # self.view.off()
            self.last_update = get_local_time()
            sleep_interval = config['SLEEP_INTERVAL']
            
            while True:
                local_time = get_local_time()
                server_time = get_server_time()

                if not self.paused:
                    self.renderer.render(server_time)

                if ((self.last_update + sleep_interval < local_time) and not self.paused):
                    self.paused = True

                    target_color = Color(0,0,0)
                    palette = Palette(self.renderer.current_color, target_color)
                    animation_start_time = local_time
                    animation_length = 100
                    easing = "ElasticEaseOut"
                    animation = Animation(animation_start_time, animation_length, easing, palette)
                    self.renderer.update_animation(animation)
                    self.last_update = local_time
                    self.ping()
                else:

                    current_animation = self.animation_list.head
                    if current_animation is not None and (current_animation.is_complete(server_time, self.renderer.render_interval)):
                        start_color = current_animation.get_target_color()
                        self.animation_list.remove()
                        self.renderer.render_color(start_color)
                        logger.log("removing")
                        new_animation = self.animation_list.head
                        if new_animation is not None:
                            new_animation.set_start_color(start_color)
                        self.renderer.update_animation(new_animation)
                        self.last_update = local_time
                        self.ping()
                        

                self.broker.check_msg()

                if self.debug_mode:
                    self.debug_pin.value((ceil(server_time/1000) % 2 == 0))
                        
        except (TypeError, OSError, Exception, MQTTException) as e:
            logger.warn(e)
            self.backup()
        except(KeyboardInterrupt) as e:
            self.view.off()
            logger.log("Exiting")
            pass