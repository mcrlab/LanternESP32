# Lantern IoT

Install Python 3
https://www.saintlad.com/install-python-3-on-mac/


Install VirtualEnv


Serial Chip
https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers

Erase the Flash
```
esptool.py -p PORT erase_flash
```
# Flash Micropython Firmware
## esp8266
```
esptool.py -p PORT --baud 115200 write_flash --flash_size=detect 0 firmware.bin
```
## esp32
```
esptool.py --chip esp32 --port /dev/cu.SLAB_USBtoUART --baud 460800 write_flash -z 0x1000 firmware/esp32-20190818-v1.11-219-gaf5c998f3.bin  
```

```
ampy -p PORT put src/lantern lantern
```

ampy -p PORT put src/main.py main.py