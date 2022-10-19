from lantern.ota_updater import OTAUpdater
from lantern.app import App

def run():
    updater = OTAUpdater('https://github.com/mcrlab/LanternESP32', 
main_dir='lantern', proxy="http://pi4.local")
    app = App(updater)
    app.main()

if __name__ == "__main__":
    run()
