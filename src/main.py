import network
import time
from neopixel import NeoPixel
from machine import Pin
from machine import unique_id
from machine import Timer
import json
from umqtt.robust import MQTTClient
from binascii import hexlify
import math
import config
import copy
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)


pin = Pin(0, Pin.OUT)   
np = NeoPixel(pin, config.NUMBER_OF_PIXELS)   
state = {
    "id":hexlify(unique_id()).decode(),
    "previous_color": {"r":0,"g":0,"b":0},
    "current_color":{"r":0,"g":0,"b":0},
    "target_color": {"r":0, "g":0,"b":0},
    "animation_time": 2000,
    "delay": 0,
    "last_instruction_time": 0
}

last_render_time = 0
last_ping_time = 0

def lerp(a, b, u):
    return math.floor((1-u) * a + u * b)

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    np[0] = RED
    np.write()    

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(config.ssid, config.password)
        while not wlan.isconnected():
            np[0] = YELLOW
            np.write()              
            time.sleep(1.0)
            pass
    print('network config:', wlan.ifconfig())
    np[0] = GREEN 
    np.write()             
    time.sleep(1.0)

def subscription_callback(topic, msg):
    state['last_instruction_time'] = time.ticks_ms()
    data = json.loads(msg)
    state['previous_color'] = copy.copy(state['current_color'])
    state['target_color'] = data['color']
    state['animation_time'] = data['time']
    state['delay'] = data['delay']

def render(now):
    global last_render_time
    
    animation_start_time = (state['last_instruction_time'] + state['delay'])
    animation_end_time = animation_start_time + state['animation_time']
    elapsed_time = now - animation_start_time
    
    if(now < animation_start_time):
        r = state['current_color']['r']
        g = state['current_color']['g']
        b = state['current_color']['b']  
    elif(now > animation_start_time and now < animation_end_time):
        r = lerp(state['previous_color']['r'], state['target_color']['r'],elapsed_time /  state['animation_time'])
        g = lerp(state['previous_color']['g'], state['target_color']['g'],elapsed_time /  state['animation_time'])
        b = lerp(state['previous_color']['b'], state['target_color']['b'],elapsed_time /  state['animation_time'])
    else:
        state['current_color']  = copy.copy(state['target_color'])
        r = state['current_color']['r']
        g = state['current_color']['g']
        b = state['current_color']['b']

    for i in range(config.NUMBER_OF_PIXELS):
        np[i] = (r, g, b)
    
    np.write() 
    last_render_time = time.ticks_ms()


def main():
    c = MQTTClient(state['id'], config.mqtt_server, config.mqtt_port, config.mqtt_user, config.mqtt_password)
    c.set_callback(subscription_callback)
    print('subscribing to mqtt')
    c.connect()
    c.publish("connect", json.dumps(state))
    c.subscribe("color/"+state['id'])
    print("subscribed")
    
    while True:
        global last_render_time
        global last_ping_time

        now = time.ticks_ms()
    
        if(now > last_render_time + config.RENDER_INTERVAL):
            render(now)

        if(now > last_ping_time + config.PING_INTERVAL):
            print("ping")
            print(json.dumps(state))
            c.publish("connect", json.dumps(state))
            last_ping_time = now

        c.check_msg()

    c.disconnect()

do_connect()
main()
