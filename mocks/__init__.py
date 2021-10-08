import paho.mqtt.client as mqtt
import time

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
        self.client.connect(self.server, self.port)
        self.client.loop_start()

    
    def subscribe(self, topic):
        self.client.subscribe(topic)
        self.client.loop_start()
    
    def publish(self, topic, data):
        self.client.publish(topic, data)
    
    def check_msg(self):
        pass
    
    def disconnect(self):
        pass


class OTAUpdater():
    def __init__(self, github_repo, module='', main_dir='main'):
        pass
    
    def download_and_install_update_if_available(self, ssid, password):
        print("downloading and installing if available")
        pass

    def check_for_update_to_install_during_next_reboot(self):
        print("updating")

    
def ticks_ms():
    return int(round(time.time() * 1000))

def unique_id():
    from random import randbytes
    return randbytes(6)

class Pin:
    OUT = 1

    def __init__(self, pin_number, direction=OUT):    
        pass

class ADC:
    def __init__(self, pin):
        pass

    def read(self):
        return -1

def reset():
    print("reboot");
    pass


def deepsleep(seconds):
    print("sleeping for ")
    print(seconds)
    print(" seconds")
    pass

class hexlify():
    def __init__(self, id):
        self.id = id
        pass
    
    def decode(self):
        return self.id

class WLAN():
    STA_IF = 0

    def __init__(self, setting):  
        self.connection_count = 0  
        pass

    def isconnected(self):
        self.connection_count = self.connection_count + 1
        return self.connection_count > 5
    
    def connect(self, ssid, password):
        pass
    
    def active(self, status):
        pass

    def ifconfig(self):
        return "ip config"


class NeoPixel(dict):
    def __init__(self, pin, numberofpixels):
        pass

    def write(self):
        print(self[0])


class MQTTException(Exception):
    pass

def mem_free():
    return 43