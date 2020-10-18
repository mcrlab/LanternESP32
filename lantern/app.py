import math
import time
import json
from .palette import Palette
from .color import Color
from .renderer import Renderer

class App():
    def __init__(self,id, config, view, broker, now, updater, reset_fn):
        self.id = id
        self.config = config
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
    

    def update_animation(self, message):
        current_time = self.now()
        data = json.loads(message)
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

        self.renderer.update(color, animation_start_time, animation_length, current_time, easing, method) 
        self.last_instruction_time = current_time


    def subscription_callback(self, topic, message):
        try:
            if "color" in topic:
                print("color update")
                self.update_animation(message)
            else:
                print("Config Update")
                self.updater.check_for_update_to_install_during_next_reboot()
                self.reset_fn()
        except Exception as inst:
            print("Error in subscription callback", inst)

    def ping(self, current_time):
        print("ping")
        update = json.dumps({
            "id" : self.id,
            "current_color" : self.renderer.get_current_color().as_object(),
            "completion" : self.renderer.get_completion(current_time),
            "easing" : self.renderer.easing,
            "method": self.renderer.method
            })
        self.broker.publish("connect", update)
        self.last_ping_time = current_time

    def main(self, retries):
        try:
            print("Starting app")
            self.broker.connect()
            self.ping(self.now())
            self.broker.subscribe("color/"+self.id)
            self.broker.subscribe("config/"+self.id)
            self.last_render_time = self.now()
            while True:
                current_time = self.now()
                
                if(((current_time - self.last_render_time) > self.config['RENDER_INTERVAL'])):
                    #if(self.renderer.should_draw(current_time)):
                    color_buffer = self.renderer.buffer_to_render(current_time)
                    self.view.render(color_buffer, current_time)
                    self.last_render_time = current_time

                if((current_time - self.last_ping_time) > self.config['PING_INTERVAL']):
                    self.ping(current_time)

                self.broker.check_msg()
                
            self.broker.disconnect()
        except TypeError as e:
            print('error', e)
        except OSError as error:
            print("Connection error", error)
            time.sleep(5)
            if(retries > 0):
                retries = retries - 1
                self.main(retries)
            else:
                print("Failed too many times")
                self.view.render(Color(0,0,255), self.now())
                time.sleep(5)
                self.view.render(Color(0,0,0), self.now())
            
            
