import socket
import struct
import utime
import network
import machine
import math

NTP_DELTA = 3155673600

RED = (255,0,0)
BLACK = (0,0,0)



import utime
from umqtt import simple
from umqtt.simple import MQTTException


class MQTTClient(simple.MQTTClient):

    DELAY = 2
    DEBUG = False
    MAX_RETRIES = 10
    def delay(self, i):
        utime.sleep(self.DELAY)

    def log(self, in_reconnect, e):
        if self.DEBUG:
            if in_reconnect:
                print("mqtt reconnect: %r" % e)
            else:
                print("mqtt: %r" % e)

    def reconnect(self):
        i = 0
        while 1:
            try:
                return super().connect(False)
            except OSError as e:
                self.log(True, e)
                i += 1
                self.delay(i)
                if(i > self.MAX_RETRIES):
                    self.log(True, "Max number of retries exceeded")
                    raise MQTTException(e)

    def publish(self, topic, msg, retain=False, qos=0):
        while 1:
            try:
                return super().publish(topic, msg, retain, qos)
            except OSError as e:
                self.log(False, e)
            self.reconnect()

    def wait_msg(self):
        while 1:
            try:
                return super().wait_msg()
            except OSError as e:
                self.log(False, e)
            self.reconnect()


def do_connect():
	wlan = network.WLAN(0)
	wlan.active(True)
	if not wlan.isconnected():
		wlan.connect("BaconBacon", "gwilbo piggins")
		while not wlan.isconnected():
			utime.sleep(1.0)
			pass

def set_time():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	NTP_QUERY=bytearray(48)
	NTP_QUERY[0]=0x1B
	addr=socket.getaddrinfo('192.168.68.111', 123)[0][-1]
	res = s.sendto(NTP_QUERY, addr)
	msg=s.recv(48)
	s.close()

	seconds = struct.unpack("!I", msg[40:44])[0]
	fract = struct.unpack("!I", msg[44:48])[0]

	ms = ((fract * 1000) >> 32) * 1000
	tm = utime.gmtime(seconds - NTP_DELTA)
	machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], ms))

def subscription_callback(topic, message):
	pass

led = machine.Pin(15, machine.Pin.OUT)
led.value(1)
do_connect()
set_time()
broker = MQTTClient("NTP",'192.168.68.111', 1883, 'lantern', 'ilovelamp')
broker.DEBUG = True
broker.set_callback(subscription_callback)
while True:
	sec = utime.localtime()[5]
	led.value(sec % 2)
	broker.check_msg()
