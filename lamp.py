import os
import threading

try:
    from lantern.ota_updater import OTAUpdater
except (ModuleNotFoundError, ImportError) as e:
    from mocks import OTAUpdater

from lantern.bootstrap import boot

def run():
    updater = OTAUpdater('https://github.com/mcrlab/LanternIoT', main_dir='lantern')
    boot(updater)



if __name__ == "__main__":
    number_of_lamps = int(os.getenv("NUMBER_OF_LAMPS", '1'))
    
    for i in range(0, number_of_lamps):
        x = threading.Thread(target=run, args=())
        x.start()    
