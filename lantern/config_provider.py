import json

class ConfigProvider():
    def __init__(self):
        
        self.config = self.load_config()
        pass
 
    def load_config(self):
        try:
            f = open("config.json", "r")
            data = json.loads(f.read())
            f.close()    
        except OSError:
            print("no local config")
        
        return data

    def update_config(self, new_config_str):
        current_config = self.config
        
        new_config = json.loads(new_config_str)
        current_config.update(new_config)
        new_config_str = json.dumps(current_config)

        f = open("config.json", "w")
        f.write(new_config_str)
        f.close()
        self.config = current_config
        
provider = ConfigProvider()
