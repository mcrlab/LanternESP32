import os
import threading
from lantern.logging import logger

try:
    from lantern.ota_updater import OTAUpdater
except (ModuleNotFoundError, ImportError) as e:
    from mocks import OTAUpdater

from lantern.app import App

def run():
    logger.DEBUG = True
    updater = OTAUpdater('https://github.com/mcrlab/LanternIoT', main_dir='lantern')
    app = App(updater)
    app.main()


if __name__ == "__main__":
    number_of_lamps = int(os.getenv("NUMBER_OF_LAMPS", '1'))
    
    for i in range(0, number_of_lamps):
        x = threading.Thread(target=run, args=())
        x.start()    
