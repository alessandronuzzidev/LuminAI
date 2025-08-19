import json
import os

class EmbeddingModelsFile:
    def __init__(self, embedding_models_path="./data/models.json"):
        self.embedding_models_path = embedding_models_path
        
    def generate_embedding_models_file(self, embedding_models_data):
        """
        Create embedding models file.
        
        :param embedding_models_data: Data of embedding models.
        """
        embedding_models_dir = os.path.dirname(self.embedding_models_path)
        os.makedirs(embedding_models_dir, exist_ok=True)
        
        with open(self.embedding_models_path, 'w') as embedding_models_file:
            json.dump(embedding_models_data, embedding_models_file, indent=4)
        print(f"Embedding models file generated at {self.embedding_models_path}")
        
