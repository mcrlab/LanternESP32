import json

class ConfigProvider():
    def __init__(self):
        
        self.config = {
            "network": self.load_network_config(),
            "runtime": self.load_runtime_config()
        }
        
        pass
 
    def load_network_config(self):
        try:
            f = open("network.config.json", "r")
            data = json.loads(f.read())
            f.close()    
        except OSError:
            print("no local config")
        
        return data

    def load_runtime_config(self):
        try:
            f = open("runtime.config.json", "r")
            data = json.loads(f.read())
            f.close()    
        except OSError:
            print("no local config")

        return data

    def update_runtime_config(self, new_config_str):
        current_config = self.config['runtime']
        
        new_config = json.loads(new_config_str)
        current_config.update(new_config)
        new_config_str = json.dumps(current_config)

        f = open("runtime.config.json", "w")
        f.write(new_config_str)
        f.close()
        self.config["runtime"] = current_config

    def update_network_config(self, new_config_str):
        current_config = self.config.network
        
        new_config = json.loads(new_config_str)
        current_config.update(new_config)
        new_config_str = json.dumps(current_config)

        f = open("network.config.json", "w")
        f.write(new_config_str)
        f.close()
        self.runtime_config = current_config
        

