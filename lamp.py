import paho.mqtt.client as mqtt
import time
from lantern.app import App
from lantern.config_provider import ConfigProvider
import os
import argparse
import threading

class Broker():
    def __init__(self, id, server, port, username, password):
        self.client = mqtt.Client(id)
        self.server = server
        self.port = port
        self.client.username_pw_set(username, password)
        
    def on_message(self, user, topic, message):
        try:
            topic = str(message.topic)
            message = str(message.payload.decode("utf-8"))
            self.callback(topic, message)

        except Exception as inst:
            print("fail", inst)

    def set_callback(self, callback):
        self.callback=callback
        self.client.on_message=self.on_message
    
    def connect(self):
        print("connecting to: ", self.server)
        self.client.connect(self.server, self.port)
        self.client.loop_start()

    
    def subscribe(self, topic):
        print("subscribing to: ", topic)
        self.client.subscribe(topic)
        self.client.loop_start()
    
    def publish(self, topic, data):
        self.client.publish(topic, data)
    
    def check_msg(self):
        pass

class View():
    def __init__(self, number_of_pixels = 5):
        self.number_of_pixels = number_of_pixels

    def render_color(self, color):
        print(color.as_hex())
        
    def render(self, color_buffer, current_time):
        print(chr(27) + "[2J")
        
        for i in range(0, len(color_buffer)):
            print(color_buffer[i].as_hex())
        pass        

class Lamp():
    def __init__(self, id):
        self.id = id

    def start(self, updater, provider):
        config = provider.get_config()        
        view = View(config['NUMBER_OF_PIXELS'])
        broker = Broker(self.id, config['mqtt_server'], config['mqtt_port'], config['mqtt_user'], config['mqtt_password'])    
        app = App(self.id, view, broker, now, updater, reset_fn, sleep_fn, provider)
        app.main()

class Updater():
    def __init__(self):
        pass
    
    def check_for_update_to_install_during_next_reboot(self):
        print("updating")


def reset_fn():
    print("reboot")
    
def sleep_fn(seconds):
    print("sleeping for ")
    print(seconds)
    print(" seconds")
    
def now():
    return int(round(time.time() * 1000))


def create_lamp(name, id):
    Lamp(name+"_"+str(i)).start(Updater(), ConfigProvider())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs='?', default="james")
    arguments = parser.parse_args()
    number_of_lamps = int(os.getenv("NUMBER_OF_LAMPS", '1'))

    for i in range(0, number_of_lamps):
        x = threading.Thread(target=create_lamp, args=(arguments.name, i))
        x.start()    
