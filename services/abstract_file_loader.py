from abc import ABC, abstractmethod
from pathlib import Path

class AbstractFileLoader(ABC):
    
    def __init__(self, file_path):
        self.file_path = file_path
    
    @abstractmethod
    def load(self, file_path):
        """
        Load the content from the specified file path.

        :param file_path: The path to the file to be loaded.
        :return: The content of the file.
        """
        pass

    @abstractmethod
    def save(self, file_path, content):
        """
        Save the content to the specified file path.

        :param file_path: The path where the content should be saved.
        :param content: The content to be saved in the file.
        """
        pass
    
    def exists(self, file_path):
        """
        Check if the specified file exists.

        :param file_path: The path to the file to check.
        :return: True if the file exists, False otherwise.
        """
        return self.file_path.exists() and self.file_path.is_file()