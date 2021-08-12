from admin.ota_updater import OTAUpdater
from admin.config_provider import ConfigProvider
from lantern.bootstrap import start


def download_and_install_update_if_available(updater):
    updater.download_and_install_update_if_available('PLUSNET-HHQJC9', 'f6db6dd64c')
  
def boot():
    provider = ConfigProvider()
    config = provider.get_config()
    updater = OTAUpdater('https://github.com/mcrlab/LanternIoT', main_dir='lantern')
    download_and_install_update_if_available(updater)
    start(updater, provider)

boot()