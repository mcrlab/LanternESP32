import json

class ConfigProvider():
    def __init__(self):
        self.config = {}
        pass
 
    def update_config(self, new_config_str):
        f = open("local_config.json", "w")
        f.write(new_config_str)
        f.close()
        

    def get_config(self):
        try:
            f = open("local_config.json", "r")
            data = json.loads(f.read())
            print(data)
            f.close()    
            for key in data.keys():
                self.config[key] = data[key]
        except OSError:
            print("no local config")

        return self.config

