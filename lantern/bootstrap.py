
from binascii import hexlify
from .app import App
from .view import View

try:
    from machine import Pin
    from machine import unique_id
    from machine import reset
    from machine import deepsleep
    from umqtt.robust import MQTTClient
    from network import WLAN
    from time import ticks_ms
except (ModuleNotFoundError, ImportError) as e:
    from mocks import WLAN
    from mocks import Pin
    from mocks import unique_id
    from mocks import reset
    from mocks import deepsleep
    from mocks import hexlify
    from mocks import Broker as MQTTClient
    from mocks import ticks_ms

from .config_provider import ConfigProvider

def now():
    return ticks_ms()


def sleep(seconds):
    print("sleeping")
    deepsleep(seconds * 1000)
     
def boot(updater):
    provider = ConfigProvider()
    network_config = provider.config['network']
    updater.download_and_install_update_if_available(network_config['ssid'], network_config['password'])
    start(provider, updater)

def start(provider, updater):
    config = provider.config['network']
    runtime = provider.config['runtime']

    id = hexlify(unique_id()).decode()

    broker = MQTTClient(id, config['mqtt_server'], config['mqtt_port'], config['mqtt_user'], config['mqtt_password'])
    broker.DEBUG = True

    view = View(Pin(runtime['VIEW_PIN'], Pin.OUT) , runtime['NUMBER_OF_PIXELS'])

    app = App(id, view, broker, updater, provider)

    app.main()
