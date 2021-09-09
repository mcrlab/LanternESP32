from lantern.ota_updater import OTAUpdater
from lantern.config_provider import ConfigProvider
from lantern.bootstrap import start


def download_and_install_update_if_available(updater, ssid, password):
    updater.download_and_install_update_if_available(ssid, password)
  
def boot():
    provider = ConfigProvider()
    network_config = provider.config['network']
    updater = OTAUpdater('https://github.com/mcrlab/LanternIoT', main_dir='lantern')
    download_and_install_update_if_available(updater, network_config['ssid'], network_config['password'])
    start(updater, provider)

boot()