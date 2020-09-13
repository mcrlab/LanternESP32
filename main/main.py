from binascii import hexlify
from machine import Pin
from config import config
from lantern.app import App
from lantern.view import View
from lantern.color import Color
from machine import unique_id
from umqtt.robust import MQTTClient
import network
import time

def now():
    return time.ticks_ms()

def do_connect(view, config):
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

def main():
    id = hexlify(unique_id()).decode()
    pin = Pin(5, Pin.OUT)  

    broker = MQTTClient(id, config['mqtt_server'], config['mqtt_port'], config['mqtt_user'], config['mqtt_password'])
    broker.DEBUG = True

    view = View(pin, config['NUMBER_OF_PIXELS'])
    do_connect(view, config)
    app = App(id, config, view, broker, now)
    app.main(10)

main()
