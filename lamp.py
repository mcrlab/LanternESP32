from lantern.logging import logger

try:
    from lantern.ota_updater import OTAUpdater
except (ModuleNotFoundError, ImportError) as e:
    from mocks import OTAUpdater
import socket
from lantern.app import App
from mocks import unique_id
from binascii import hexlify

def run():
    logger.DEBUG = True
    updater = OTAUpdater('https://github.com/mcrlab/LanternIoT', main_dir='lantern')
    hostname = socket.gethostname()
    print(hostname)
    app = App(updater, hostname)
    app.main()


if __name__ == "__main__":
    try:
        run()  
    except KeyboardInterrupt:
        print("cleanup")