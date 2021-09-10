try:
    from lantern.ota_updater import OTAUpdater
except (ModuleNotFoundError, ImportError) as e:
    from mocks import OTAUpdater

from lantern.bootstrap import boot

def run():
    updater = OTAUpdater('https://github.com/mcrlab/LanternIoT', main_dir='lantern')
    boot(updater)

if __name__ == "__main__":
    run()