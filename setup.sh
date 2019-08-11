!#bin/bash

ampy -p $PORT put src/config.py config.py
ampy -p $PORT put lib/copy.py copy.py
ampy -p $PORT put lib/types.py types.py
ampy -p $PORT put src/main.py main.py