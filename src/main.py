from binascii import hexlify
from machine import Pin
from app import App
from view import View
from app import do_connect
from machine import unique_id

id = hexlify(unique_id()).decode()
pin = Pin(0, Pin.OUT)  

view = View(pin, 16)
do_connect(view)
app = App(id, view)
app.main()
