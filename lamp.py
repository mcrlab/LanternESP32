import paho.mqtt.client as mqtt
import time
import json
from lantern.main.app import App

config = {
    "ssid" : 'twguest',
    "password" : 'heroic crab mammal dual swig',
    "mqtt_server" : '127.0.0.1',
    "mqtt_port" : 1883,
    "mqtt_user" : "lantern",
    "mqtt_password" : "ilovelamp",
    "NUMBER_OF_PIXELS" : 20,
    "RENDER_INTERVAL" : 50,
    "PING_INTERVAL" : 10000,
}


class Broker():
    def __init__(self, id):
        self.client = mqtt.Client(id)
        self.client.username_pw_set("lantern", "ilovelamp")
        
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
        self.client.connect(config['mqtt_server'])
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

    def render(self, color_buffer, current_time):
        return
        print(chr(27) + "[2J")
        
        for i in range(0, len(color_buffer)):
            print(color_buffer[i].as_hex())
        

class Lamp():
    def __init__(self, id):
        self.id = id

    def start(self, updater):
        view = View(config['NUMBER_OF_PIXELS'])
        broker = Broker(self.id)    
        app = App(self.id, config, view, broker, now, updater)
        app.main(1)

class Updater():
    def __init__(self):
        pass
    
    def check_for_update_to_install_during_next_reboot(self):
        print("updating")
        

    
def now():
    return int(round(time.time() * 1000))

Lamp("james").start(Updater())