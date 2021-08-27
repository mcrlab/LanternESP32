import math
import time
import json
from .palette import Palette
from .color import Color
from .renderer import Renderer
from .colors import default_colors
import network

class App():
    def __init__(self,id, view, broker, now, updater, reset_fn, sleep_fn, provider, WLAN):
        self.id = id
        self.view = view
        self.broker = broker
        self.now = now
        self.renderer = Renderer(view.number_of_pixels)
        self.last_instruction_time = 0
        self.last_ping_time = 0 
        self.last_render_time = 0
        self.broker.set_callback(self.subscription_callback)
        self.updater = updater
        self.reset_fn = reset_fn
        self.sleep_fn = sleep_fn
        self.provider = provider
        self.version = ""
        self.paused = False   
        self.config = provider.get_config() 
        self.WLAN = WLAN

    def update_animation(self, data):
        current_time = self.now()

        color = Color(data['color']['r'],data['color']['g'],data['color']['b'])
        animation_length = data['time']
        animation_start_time = current_time + data['delay']

        if 'easing' in data:
            easing = data['easing']
        else:
            easing = "ElasticEaseOut"

        if 'method' in data:
            method = data['method']
        else:
            method = "fill"

        self.renderer.update(color, animation_start_time, animation_length, easing, method) 
        self.last_instruction_time = current_time


    def subscription_callback(self, topic, message):
        try:
            self.paused = False
            self.last_update = self.now()
            if "color" in topic:
                print("color update")
                data = json.loads(message)
                self.update_animation(data)
            elif "update" in topic:
                print("Firmware Update")
                self.broker.disconnect()
                self.updater.check_for_update_to_install_during_next_reboot()
                print("checked")
                self.reset_fn()
            elif "config" in topic:
                print("config update")
                self.provider.update_config(message)
                self.reset_fn()
            elif "sleep" in topic:
                self.view.render_color(Color(0,0,0))  
                data = json.loads(message)
                self.sleep_fn(data["seconds"])
            elif "restart" in topic:
                self.view.render_color(Color(0,0,0))  
                print("restarting")
                self.reset_fn()
            else:
                print("unknown command")
        except Exception as inst:
            print("Error in subscription callback", inst)

    def ping(self, current_time):
        update = json.dumps({
            "id" : self.id,
            "current_color" : self.renderer.get_current_color().as_object(),
            "pixels": self.config['NUMBER_OF_PIXELS'],
            "version": self.version
            })
        self.broker.publish("connect", update)
        self.last_ping_time = current_time

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
        self.last_update = self.now()
        while True:
            current_time = self.now()
            if (self.last_update + 5000 < current_time):

                data = {
                    "color": default_colors[color_int],
                    "time": 2000,
                    "delay": 10
                }
                self.update_animation(data)
                self.last_update = current_time
                color_int = color_int + 1
                if(color_int >= len(default_colors)):
                    color_int = 0

            self.check_and_render(current_time)

    def subscribe(self):
        print("subscribing")
        self.broker.subscribe("color/"+self.id)
        self.broker.subscribe("update/"+self.id)
        self.broker.subscribe("config/"+self.id)
        self.broker.subscribe("restart/"+self.id)
        self.broker.subscribe("sleep/"+self.id)

    def check_and_render(self, current_time):
        if(((current_time - self.last_render_time) > self.config['RENDER_INTERVAL'])):
            if(self.renderer.should_draw(current_time)):
                color_buffer = self.renderer.buffer_to_render(current_time)
                self.view.render(color_buffer, current_time)
                self.last_render_time = current_time
    
    
    def main(self):
        self.set_version()
        try:
            print("Starting app")
            
            wlan = self.WLAN(0)
            wlan.active(True)
            time.sleep(1.0)
            if not wlan.isconnected():
                print('connecting to network...')
                wlan.connect(self.config['ssid'], self.config['password'])
                while not wlan.isconnected():    
                    time.sleep(1.0)
                    pass

            print('network config:', wlan.ifconfig()) 
            time.sleep(1.0)

            self.broker.connect()
            self.subscribe()
            self.ping(self.now())
            
            self.last_render_time = self.now()
            self.view.render_color(Color(0,0,0))  
            self.last_update = self.now()

            while True:
                current_time = self.now()
                if ((self.last_update + self.config['SLEEP_INTERVAL'] < current_time) and not self.paused):
                    self.paused = True
                    self.renderer.update(Color(0,0,0), current_time, 1000, "ElasticEaseOut", "fill")
                    self.last_update = current_time
                else:
                    self.check_and_render(current_time)

                if((current_time - self.last_ping_time) > self.config['PING_INTERVAL']):
                    self.ping(current_time)

                self.broker.check_msg()
                
            self.broker.disconnect()

        except TypeError as e:
            print('error', e)
        except OSError as error:
            print("Connection error", error)
        finally:
            print("Error Caught")
            self.backup()