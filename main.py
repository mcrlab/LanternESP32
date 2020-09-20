from lantern.main.ota_updater import OTAUpdater
from lantern.main.main import start as app

o = OTAUpdater('https://github.com/mcrlab/LanternIoT')

def download_and_install_update_if_available():
    o.download_and_install_update_if_available('PLUSNET-HHQJC9', 'f6db6dd64c')

def start():
    app(o)

def boot():
    download_and_install_update_if_available()
    start()

boot()