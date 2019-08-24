import math
import time
import json

import network
from machine import Timer
from umqtt.robust import MQTTClient

from lantern.config import config
from lantern.view import View
from lantern.palette import Palette
from lantern.color import Color

def do_connect(view):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    view.render(Color(255,0,0), now())
    time.sleep(1.0)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(config['ssid'], config['password'])
        while not wlan.isconnected():    
            view.render(Color(255,255,0), now()) 
            time.sleep(1.0)
            pass
    print('network config:', wlan.ifconfig())
    view.render(Color(0,255,0), now())     
    time.sleep(1.0)


def now():
    return time.ticks_ms()


class App():
    def __init__(self,id, view):
        self.id = id

        self.palette = Palette()

        self.last_instruction_time = 0
        self.last_ping_time = 0 

        self.c = MQTTClient(self.id, config['mqtt_server'], config['mqtt_port'], config['mqtt_user'], config['mqtt_password'])
        self.c.DEBUG = True
        self.c.set_callback(self.subscription_callback)
        self.view = view

    def subscription_callback(self, topic, message):
        current_time = now()
        data = json.loads(message)
        color = Color(data['color']['r'],data['color']['g'],data['color']['b'])
        animation_length = data['time']
        animation_start_time = current_time + data['delay']

        self.palette.update(color, animation_length, animation_start_time) 
        self.last_instruction_time = current_time

    def ping(self):
        current_time = now()
        update = json.dumps({
            "id" : self.id,
            "current_color" : self.palette.color_to_render(current_time).as_object()
            })
        self.c.publish("connect", update)
        self.last_ping_time = current_time

    def main(self):
        self.c.connect()
        self.ping()
        self.c.subscribe("color/"+self.id)

        while True:
            current_time = now()

            if(current_time > self.view.last_render_time + config['RENDER_INTERVAL']):
                color = self.palette.color_to_render(current_time)
                self.view.render(color, current_time)

            if(current_time > self.last_ping_time + config['PING_INTERVAL']):
                self.ping()

            self.c.check_msg()

        self.c.disconnect()
