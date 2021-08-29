import json

class ConfigProvider():
    def __init__(self):
        self.config = {}
        self.network_config = {}
        self.runtime_config = {}
        pass
 
    def get_network_config(self):
        try:
            f = open("network.config.json", "r")
            data = json.loads(f.read())
            f.close()    
            for key in data.keys():
                self.network_config[key] = data[key]
        except OSError:
            print("no local config")

        return self.network_config

    def get_runtime_config(self):
        try:
            f = open("runtime.config.json", "r")
            data = json.loads(f.read())
            f.close()    
            for key in data.keys():
                self.runtime_config[key] = data[key]
        except OSError:
            print("no local config")

        return self.runtime_config

    def update_runtime_config(self, new_config_str):
        current_config = self.get_runtime_config()
        
        new_config = json.loads(new_config_str)
        current_config.update(new_config)
        new_config_str = json.dumps(current_config)

        f = open("runtime.config.json", "w")
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

