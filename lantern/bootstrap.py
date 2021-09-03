from binascii import hexlify
from .app import App
from .view import View

from machine import Pin
from machine import unique_id
from machine import reset
from machine import deepsleep
from umqtt.robust import MQTTClient
from network import WLAN

import time


def now():
    return time.ticks_ms()


def sleep(seconds):
    print("sleeping")
    deepsleep(seconds * 1000)

def start(updater, provider):
    config = provider.network_config
    runtime = provider.runtime_config
    id = hexlify(unique_id()).decode()

    broker = MQTTClient(id, config['mqtt_server'], config['mqtt_port'], config['mqtt_user'], config['mqtt_password'])
    broker.DEBUG = True

    view = View(Pin(runtime['VIEW_PIN'], Pin.OUT) , runtime['NUMBER_OF_PIXELS'])

    app = App(id, view, broker, now, updater, reset, sleep, provider, WLAN)

    app.main()
