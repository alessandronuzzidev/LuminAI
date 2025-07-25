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
    def exists(self, file_path):
        """
        Check if the specified file exists.

        :param file_path: The path to the file to check.
        :return: True if the file exists, False otherwise.
        """
        return self.file_path.exists() and self.file_path.is_file()