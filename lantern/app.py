import time
import json
from .color import Color
from .renderer import Renderer
from .colors import hex_colors
from .view import View
from .config_provider import ConfigProvider
from binascii import hexlify
try:
    from machine import unique_id
    from machine import Pin
    from machine import reset
    from machine import deepsleep
    from network import WLAN
    from time import ticks_ms
    from .mqtt import MQTTClient
    from umqtt.simple import MQTTException
except (ModuleNotFoundError, ImportError) as e:
    from mocks import unique_id
    from mocks import Broker as MQTTClient    
    from mocks import Pin    
    from mocks import WLAN
    from mocks import reset
    from mocks import deepsleep
    from mocks import ticks_ms
    from mocks import MQTTException

class App():
    def __init__(self, updater):

        self.provider = ConfigProvider()
        self.updater = updater

        runtime = self.provider.config['runtime']
        config = self.provider.config['network']


        self.id = hexlify(unique_id()).decode()
        self.broker = MQTTClient(self.id, config['mqtt_server'], config['mqtt_port'], config['mqtt_user'], config['mqtt_password'])
        self.broker.DEBUG = True

        self.view = View(Pin(runtime['VIEW_PIN'], Pin.OUT) , runtime['NUMBER_OF_PIXELS'])
    
        self.renderer = Renderer(runtime['NUMBER_OF_PIXELS'])
        self.last_instruction_time = 0
        self.last_ping_time = 0 
        self.last_render_time = 0
        self.broker.set_callback(self.subscription_callback)
        self.updater = updater
        self.version = ""
        self.paused = False   


    def update_animation(self, data):
        current_time = ticks_ms()

        color = Color(0,0,0)
        color.from_hex(data['color'])
        animation_length = data['time']
        animation_start_time = current_time + data['delay']

        if 'easing' in data:
            easing = data['easing']
        else:
            easing = "ElasticEaseOut"

        self.renderer.update(color, animation_start_time, animation_length, easing) 
        self.last_instruction_time = current_time


    def subscription_callback(self, topic, message):
        try:
            self.paused = False
            self.last_update = ticks_ms()
            if "color" in topic:
                print("Color update")
                data = json.loads(message)
                self.update_animation(data)
            elif "update" in topic:
                print("Firmware Update")
                self.view.off()  
                self.broker.disconnect()
                self.updater.check_for_update_to_install_during_next_reboot()
                print("checked")
                reset()
            elif "config" in topic:
                print("config update")
                print(message)
                self.provider.update_runtime_config(message)
            elif "sleep" in topic:
                self.view.off()  
                data = json.loads(message)
                deepsleep(data["seconds"] * 1000)
            elif "restart" in topic:
                self.view.off() 
                print("restarting")
                reset()
            else:
                print("unknown command")
        except Exception as inst:
            print("Error in subscription callback", inst)

    def ping(self, current_time):
        update = json.dumps({
            "id" : self.id,
            "current_color" : self.renderer.get_current_color().as_hex()
            })
        self.broker.publish("ping", update)
        self.last_ping_time = current_time


    def connect(self):
        update = json.dumps({
            "id" : self.id,
            "current_color" : self.renderer.get_current_color().as_hex(),
            "version": self.version,
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
        print("starting backup sequence")
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
                    "color": color.as_object(),
                    "time": 2000,
                    "delay": 10
                }
                self.update_animation(data)
                self.last_update = current_time
                color_int = color_int + 1
                if(color_int >= len(hex_colors)):
                    color_int = 0

            self.check_and_render(current_time)
        print("Restarting")
        self.view.off()
        reset()

    def subscribe(self):
        print("Subscribing")
        self.broker.subscribe("color/"+self.id)
        self.broker.subscribe("update/"+self.id)
        self.broker.subscribe("config/"+self.id)
        self.broker.subscribe("restart/"+self.id)
        self.broker.subscribe("sleep/"+self.id)

    def check_and_render(self, current_time, render_interval):
        if(((current_time - self.last_render_time) > render_interval)):
            if(self.renderer.should_draw(current_time)):
                color_buffer = self.renderer.buffer_to_render(current_time)
                self.view.render(color_buffer, current_time)
                self.last_render_time = current_time
    
    
    def main(self):
        config = self.provider.config['network']
        self.updater.download_and_install_update_if_available(config['ssid'], config['password'])
        self.set_version()
        try:
            print("Starting app")
            config = self.provider.config['network']
            wlan = WLAN(0)
            wlan.active(True)
            time.sleep(1.0)
            if not wlan.isconnected():
                print('connecting to network...')
                wlan.connect(config['ssid'], config['password'])
                while not wlan.isconnected():    
                    time.sleep(1.0)
                    pass

            print('network config:', wlan.ifconfig()) 
            time.sleep(1.0)

            self.broker.connect()
            self.subscribe()
            self.connect()
            
            self.last_render_time = ticks_ms()
            self.view.off()
            self.last_update = ticks_ms()

            sleep_interval = self.provider.config['runtime']['SLEEP_INTERVAL']
            ping_interval = self.provider.config['runtime']['PING_INTERVAL']
            render_interval = self.provider.config['runtime']['RENDER_INTERVAL']

            while True:
                current_time = ticks_ms()
                if ((self.last_update + sleep_interval < current_time) and not self.paused):
                    self.paused = True
                    self.renderer.update(Color(0,0,0), current_time, 1000, "ElasticEaseOut", "fill")
                    self.last_update = current_time
                else:
                    self.check_and_render(current_time, render_interval)

                if((current_time - self.last_ping_time) >  ping_interval):
                    self.ping(current_time)

                self.broker.check_msg()
                


        except (TypeError, OSError, Exception, MQTTException) as e:
            print('Error', e)
        finally:
            print("Error Caught")
            self.backup()