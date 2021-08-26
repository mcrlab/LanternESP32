# Lantern IoT

Lantern is a simple IoT project to get started with MQTT, basic electronics and IoT. It uses MicroPython

## Install Dependencies
Install Python 3

https://www.saintlad.com/install-python-3-on-mac/


**Install VirtualEnv**

https://sourabhbajaj.com/mac-setup/Python/virtualenv.html


**Install Picocom**

```
brew install picocom
```

## Set up Virtual Env
```
virtualenv venv

source venv/bin/activate

pip install -r requirements.txt
```

## Install Micropython Firmware

### Install Serial Chip Drivers

https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers

### Connect to device

find the serial port the device is connected to. It will mount on a mac something similar to:

/dev/cu.wcch********

set this as an environment file either in a .env or run:

```
export AMPY_PORT=/dev/cu.wc******
```


### Erase the Flash
```
esptool.py -p $AMPY_PORT erase_flash
```
### Flash Micropython Firmware


**Chip esp8266**
```
esptool.py -p $AMPY_PORT --baud 115200 write_flash --flash_size=detect 0 firmware.bin
```

**Chip esp32**
```
esptool.py --chip esp32 --port $AMPY_PORT --baud 460800 write_flash -z 0x1000 firmware/esp32-20210623-v1.16.bin 
```

## Connect to the device

```
picocom $AMPY_PORT -b 115200
```

command a x to exit


## Provision the device
We need to install the python libraries that run the light. These will cover connecting to Wifi, subscribing to the MQTT broker and turning the lights on and off.

We're going to use ampy, a python library to upload our source files to the device.


```
ampy put src/lantern lantern

ampy put src/main.py main.py
```


#Connect the WS8212 Lights

Disconnect the device from your laptop and take the LEDs and connect them to the following device pins

red to 3v
black to gnd
data to D1

## Reboot the device
Connect back to power.

The light should: 
 - turn red for a second after powering on
 - turn yellow whilst it connects to the wifi
 - turn green as it subscribes to the MQTT broker  