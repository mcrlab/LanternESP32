from lantern.ota_updater import OTAUpdater
from lantern.bootstrap import start

updater = OTAUpdater('https://github.com/mcrlab/LanternIoT', main_dir='lantern')

def download_and_install_update_if_available():
    updater.download_and_install_update_if_available('PLUSNET-HHQJC9', 'f6db6dd64c')

def run():
    start(updater)

def boot():
    download_and_install_update_if_available()
    run()

boot()