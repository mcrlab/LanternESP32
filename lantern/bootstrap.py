from binascii import hexlify
from .config import config
from .app import App
from .view import View
from .color import Color
from machine import Pin
from machine import unique_id
from machine import reset
from umqtt.robust import MQTTClient
import network
import time

def now():
    return time.ticks_ms()

def do_connect(view, config):
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


def start(updater):
    id = hexlify(unique_id()).decode()
    pin = Pin(5, Pin.OUT)  

    broker = MQTTClient(id, config['mqtt_server'], config['mqtt_port'], id, id)
    broker.DEBUG = True
    view = View(pin, config['NUMBER_OF_PIXELS'])
    do_connect(view, config)
    app = App(id, config, view, broker, now, updater, reset)
    app.main(10)
