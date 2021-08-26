!#bin/bash
echo "Erasing flash"
esptool.py -p $AMPY_PORT erase_flash
sleep 1
echo "Flashing firmware"
esptool.py --chip esp32 --port $AMPY_PORT --baud 460800 write_flash -z 0x1000 firmware/esp32-20210623-v1.16.bin
sleep 1
echo "Uploading lantern library"
ampy put lantern/
sleep 1
echo "Uploading config"
ampy put local_config.json
sleep 1
echo "Uploading main script"
ampy put main.py
echo "All done!"