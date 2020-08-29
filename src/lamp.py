import paho.mqtt.client as mqtt
import time
import json
from lantern.app import App
import tkinter
from tkinter import *

config = {
    "ssid" : 'twguest',
    "password" : 'heroic crab mammal dual swig',
    "mqtt_server" : '127.0.0.1',
    "mqtt_port" : 1883,
    "mqtt_user" : "lantern",
    "mqtt_password" : "ilovelamp",
    "NUMBER_OF_PIXELS" : 16,
    "RENDER_INTERVAL" : 500,
    "PING_INTERVAL" : 10000,
}


class Broker():
    def __init__(self):
        self.c = mqtt.Client("Lamp")
        self.c.username_pw_set("lantern", "ilovelamp")
        
    def on_message(self, user, topic, message):
        try:
            message = str(message.payload.decode("utf-8"))
            self.callback(topic, message)

        except Exception as inst:
            print("fail", inst)

    def set_callback(self, callback):
        self.callback=callback
        self.c.on_message=self.on_message
    
    def connect(self):
        self.c.connect(config['mqtt_server'])
        self.c.loop_start()

    
    def subscribe(self, topic):
        self.c.subscribe(topic)
        self.c.loop_start()
    
    def publish(self, topic, data):
        self.c.publish(topic, data)
    
    def check_msg(self):
        pass

class View():
    
    def __init__(self):
        self.last_render_time = 0
        #self.root = tkinter.Tk()
        
    def render(self, color, current_time):
        self.last_render_time=time.time()
        print(color.as_hex())
        #self.root.configure(background=color.as_hex())
        

class Lamp():
    def __init__(self, id):
        self.id = id
        pass

    def start(self):
        view = View()
        broker = Broker()    
        app = App(self.id, config, view, broker, now)
        app.main(1)


def now():
    return int(round(time.time() * 1000))

Lamp("james").start();