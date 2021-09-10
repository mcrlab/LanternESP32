from .app import App
from .config_provider import ConfigProvider

def boot(updater):
    provider = ConfigProvider()
    network_config = provider.config['network']
    updater.download_and_install_update_if_available(network_config['ssid'], network_config['password'])
    app = App(updater, provider)
    app.main()

