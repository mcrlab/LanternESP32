import machine
import time
led = machine.Pin(15, machine.Pin.OUT)
while True:
	led.value(not led.value())
	time.sleep(1)

