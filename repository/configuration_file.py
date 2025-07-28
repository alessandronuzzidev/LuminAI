import json
import os

class ConfigurationFile:
    def __init__(self, config_path="./data/config.json"):
        self.config_path = config_path

    def generate_config_file(self, config_data):
        config_dir = os.path.dirname(self.config_path)
        os.makedirs(config_dir, exist_ok=True)
        
        with open(self.config_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        print(f"Configuration file generated at {self.config_path}")
        
    def load_config_file(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as config_file:
                return json.load(config_file)
        else:
            print(f"Configuration file not found at {self.config_path}")
            return None