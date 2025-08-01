from services.abstract_file_loader import AbstractFileLoader
import os
import yaml

class YAMLLoader(AbstractFileLoader):
    
    def __init__(self):
        super().__init__()
        
    def load(self, file_path, file_name):
        """
        Load the content from the specified YAML file path.
        :param file_path: The path to the YAML file to check.
        :param file_name: The name of the YAML file to check.
        :return: A dictionary containing the file's metadata and content.
        """
        full_path = os.path.join(file_path, file_name)
        with open(full_path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
        
        doc = {
            "name": file_name,
            "path": full_path,
            "extension": "yaml",
            "content": content.strip().replace("\n", " "),
            "size_bytes": os.path.getsize(full_path)
        }
        
        return doc
    
    def exists(self, file_path, file_name):
        """
        Check if the specified YAML file exists.

        :param file_path: The path to the YAML file to check.
        :param file_name: The name of the YAML file to check.
        :return: True if the file exists, False otherwise.
        """
        return os.path.exists(os.path.join(file_path, file_name)) and os.path.isfile(os.path.join(file_path, file_name))