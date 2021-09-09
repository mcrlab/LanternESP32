!#bin/bash
echo "Upoading mqtt libs"
ampy put lib
sleep 1     
echo "Uploading lantern library"
ampy put lantern/
sleep 1
echo "Uploading runtime config"
ampy put runtime.config.json runtime.config.json
sleep 1
echo "Uploading network config"
ampy put network.config.json network.config.json
sleep 1
echo "Uploading main script"
ampy put main.py
echo "All done!"