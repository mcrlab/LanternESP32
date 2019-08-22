from binascii import hexlify
import math
import config
from color import Color
from color import calculate_color
import time
import json

import network
from neopixel import NeoPixel
from machine import Pin
from machine import unique_id
from machine import Timer
from umqtt.robust import MQTTClient

def do_connect(view):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    view.render(Color(255,0,0))
    time.sleep(1.0)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(config.ssid, config.password)
        while not wlan.isconnected():    
            view.render(Color(255,255,0)) 
            time.sleep(1.0)
            pass
    print('network config:', wlan.ifconfig())
    view.render(Color(0,255,0))     
    time.sleep(1.0)

class View():
    def __init__(self, pin, number_of_pixels):
        self.number_of_pixels = number_of_pixels
        self.pin = pin 
        self.np = NeoPixel(self.pin, self.number_of_pixels)  
        self.last_render_time = 0
        
    def render(self, color):
        for i in range(self.number_of_pixels):
            self.np[i] = color.instruction()
            self.np.write()
            self.last_render_time = 0

def now():
    return time.ticks_ms()

class App():
    def __init__(self,id, view):
        self.id = id

        self.current_color = Color(0,0,0)
        self.previous_color = Color(0,0,0)
        self.target_color = Color(0,0,0)
        
        self.delay = 0
        self.last_instruction_time = 0
        self.last_ping_time = 0 
        self.animation_time = 0

        self.c = MQTTClient(self.id, config.mqtt_server, config.mqtt_port, config.mqtt_user, config.mqtt_password)
        self.c.DEBUG = True
        self.c.set_callback(self.subscription_callback)
        self.view = view

    def subscription_callback(self, topic, message):
        data = json.loads(message)
        self.previous_color = Color(self.current_color.r, self.current_color.g, self.current_color.b)
        self.target_color   = Color(data['color']['r'],data['color']['g'],data['color']['b'])
        self.animation_time = data['time']
        self.delay          = data['delay']
        self.last_instruction_time = now()


    def ping(self):
        self.c.publish("connect", json.dumps({
            "id" : self.id,
            "current_color" : self.current_color.instruction()
            }))
        self.last_ping_time = now()


    def animate(self, current_time):

        animation_start_time = self.last_instruction_time + self.delay

        color_to_render = calculate_color(current_time, 
                                            self.animation_time, 
                                            animation_start_time, 
                                            self.previous_color,
                                            self.current_color,
                                            self.target_color)
        return color_to_render

    def main(self):
        self.c.connect()
        self.ping()
        self.c.subscribe("color/"+self.id)

        while True:
            current_time = now()

            if(current_time > self.view.last_render_time + config.RENDER_INTERVAL):
                self.current_color = self.animate(current_time)
                self.view.render(self.current_color)

            if(current_time > self.last_ping_time + config.PING_INTERVAL):
                self.ping()

            self.c.check_msg()

        self.c.disconnect()

id = hexlify(unique_id()).decode()
pin = Pin(0, Pin.OUT)  

view = View(pin, 16)
do_connect(view)
app = App(id, view)
app.main()
