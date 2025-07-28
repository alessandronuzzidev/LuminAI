import json
import os

class EmbeddingModelsFile:
    def __init__(self, embedding_models_path="./data/models.json"):
        self.embedding_models_path = embedding_models_path
        
    def generate_embedding_models_file(self, embedding_models_data):
        embedding_models_dir = os.path.dirname(self.embedding_models_path)
        os.makedirs(embedding_models_dir, exist_ok=True)
        
        with open(self.embedding_models_path, 'w') as embedding_models_file:
            json.dump(embedding_models_data, embedding_models_file, indent=4)
        print(f"Embedding models file generated at {self.embedding_models_path}")
        
    def load_embedding_models_file(self):
        if os.path.exists(self.embedding_models_path):
            with open(self.embedding_models_path, 'r') as embedding_models_file:
                data = json.load(embedding_models_file)
                if isinstance(data, list):
                    return [item for item in data if isinstance(item, dict)]
                elif isinstance(data, dict):
                    return [data]
                else:
                    print("Unexpected data format in embedding models file.")
                    return []
        else:
            print(f"Embedding models file not found at {self.embedding_models_path}")
            return None