from ota_update.main.ota_updater import OTAUpdater
from main.main import main as app

def download_and_install_update_if_available():
    o = OTAUpdater('https://github.com/mcrlab/LanternIoT')
    o.download_and_install_update_if_available('PLUSNET-HHQJC9', 'f6db6dd64c')

def start():
    app()

def boot():
    download_and_install_update_if_available()
    start()


boot()