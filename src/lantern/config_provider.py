import json
import os
class ConfigProvider():
    def __init__(self):
        self.config = self.get_default_config()
        pass
    
    def get_default_config(self):
        f = open( os.path.join(os.getcwd(), os.path.dirname(__file__),"config.json") , "r")
        config = json.loads(f.read())
        f.close()
        return config

    def update_config(self, new_config_str):
        f = open("local_config.json", "w")
        f.write(new_config_str)
        f.close()

    def get_config(self):
        try:
            f = open("local_config.json", "r")
            data = json.loads(f.read())
            f.close()    
            for key in data.keys():
                self.config[key] = data[key]
        except OSError:
            print("no local config")

        return self.config

