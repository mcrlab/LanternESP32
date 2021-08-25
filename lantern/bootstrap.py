from binascii import hexlify
from .app import App
from .view import View
from .color import Color
from machine import Pin
from machine import unique_id
from machine import reset
from machine import deepsleep
from umqtt.robust import MQTTClient
import network
import time
import json

def now():
    return time.ticks_ms()

def connect_to_wifi(view, config):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    view.render_color(Color(255,0,0))
    time.sleep(1.0)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(config['ssid'], config['password'])
        while not wlan.isconnected():    
            view.render_color(Color(255,255,0))
            time.sleep(1.0)
            pass
    print('network config:', wlan.ifconfig())
    view.render_color(Color(0,255,0))    
    time.sleep(1.0)

def sleep(seconds):
    deepsleep(seconds * 1000)

def start(updater, provider):
    config = provider.get_config()
    id = hexlify(unique_id()).decode()
    pin = Pin(5, Pin.OUT)  
    broker = MQTTClient(id, config['mqtt_server'], config['mqtt_port'], config['mqtt_user'], config['mqtt_password'])
    broker.DEBUG = True
    view = View(pin, config['NUMBER_OF_PIXELS'])
    connect_to_wifi(view, config)
    app = App(id, view, broker, now, updater, reset, sleep, provider)
    app.main(10)
