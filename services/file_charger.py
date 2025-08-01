import json
import os

class FileCharger:
    
    def __init__(self, path="data/config.json"):
        json_path = path
        with open(json_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            
        self.root_dir = config["path"]
        
    def execute(self):
        if self.root_dir:
            for dirpath, dirnames, filenames in os.walk(self.root_dir):
                print(f"Directorio actual: {dirpath}")
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    print(f"Archivo: {full_path}")