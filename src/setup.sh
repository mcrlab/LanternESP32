!#bin/bash

esptool.py erase_flash
esptool.py --baud 115200 write_flash --flash_size=detect 0 firmware/esp8266-20190529-v1.11.bin
ampy -p /dev/cu.wchusbserial14310 put src/config.py config.py
ampy -p /dev/cu.wchusbserial14310 put src/main.py main.py