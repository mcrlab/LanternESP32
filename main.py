try:
    from lantern.ota_updater import OTAUpdater
except (ModuleNotFoundError, ImportError) as e:
    from mocks import OTAUpdater

from lantern.bootstrap import boot


updater = OTAUpdater('https://github.com/mcrlab/LanternIoT', main_dir='lantern')
boot(updater)