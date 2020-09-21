from lantern.main import start as app
from lantern.ota_updater import OTAUpdater
updater = OTAUpdater('https://github.com/mcrlab/LanternIoT', main_dir='lantern')
a = updater.http_client.get("https://api.github.com/repos/mcrlab/LanternIoT/contents/lantern/main?ref=refs/tags/1.0.2")

def download_and_install_update_if_available():
    updater.download_and_install_update_if_available('PLUSNET-HHQJC9', 'f6db6dd64c')

def start():
    app(updater)

def boot():
    download_and_install_update_if_available()
    start()

boot()