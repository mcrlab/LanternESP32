import math
import time
import json

from machine import Timer
from umqtt.robust import MQTTClient

from lantern.view import View
from lantern.palette import Palette
from lantern.color import Color


def now():
    return time.ticks_ms()

class App():
    def __init__(self,id, config, view):
        self.id = id
        self.config = config
        self.palette = Palette()

        self.last_instruction_time = 0
        self.last_ping_time = 0 

        self.c = MQTTClient(self.id, self.config['mqtt_server'], self.config['mqtt_port'], self.config['mqtt_user'], self.config['mqtt_password'])
        self.c.DEBUG = True
        self.c.set_callback(self.subscription_callback)
        self.view = view

    def subscription_callback(self, topic, message):
        current_time = now()
        data = json.loads(message)
        color = Color(data['color']['r'],data['color']['g'],data['color']['b'])
        animation_length = data['time']
        animation_start_time = current_time + data['delay']
        self.palette.update(color, animation_start_time, animation_length) 
        self.last_instruction_time = current_time

    def ping(self):
        current_time = now()
        update = json.dumps({
            "id" : self.id,
            "current_color" : self.palette.color_to_render(current_time).as_object()
            })
        self.c.publish("connect", update)
        self.last_ping_time = current_time

    def main(self, retries):
        try:
            self.c.connect()
            self.ping()
            self.c.subscribe("color/"+self.id)

            while True:
                current_time = now()

                if(current_time > self.view.last_render_time + self.config['RENDER_INTERVAL']):
                    color = self.palette.color_to_render(current_time)
                    self.view.render(color, current_time)
                    print("rendering")

                if(current_time > self.last_ping_time + self.config['PING_INTERVAL']):
                    self.ping()

                self.c.check_msg()

            self.c.disconnect()
        except OSError:
            print("Connection error")
            time.sleep(5)
            if(retries > 0):
                retries = retries - 1
                self.main(retries)
            else:
                print("Failed too many times")
                self.view.render(Color(0,0,255), now())
                time.sleep(5)
                self.view.render(Color(0,0,0), now())
            
            
