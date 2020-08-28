import paho.mqtt.client as mqtt
import time
import json
from lantern.color import Color
from lantern.palette import Palette
from lantern.app import App

id = "james"
palette = Palette()

def now():
    return 1

def on_message(client, userdata, message):
    try:
        current_time = now()
        data = json.loads(str(message.payload.decode("utf-8")))
        color = Color(data['color']['r'],data['color']['g'],data['color']['b'])
        animation_length = data['time']
        animation_start_time = current_time + data['delay']
        palette.update(color, animation_start_time, animation_length, current_time) 
        print("Update recieved")
    except:
        print("Error in subscription callback")

client = mqtt.Client("Lamp")
client.username_pw_set("lantern", "ilovelamp")
client.connect("127.0.0.1")
client.on_message=on_message

client.subscribe("color/" + id)

client.loop_start()

while True:
    current_time = 0
    update = json.dumps({
        "id" : id,
        "current_color" : palette.color_to_render(current_time).as_object()
    })
    client.publish("connect",update)
    time.sleep(5)