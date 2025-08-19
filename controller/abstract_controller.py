from abc import ABC, abstractmethod
from pathlib import Path

class AbstractController(ABC):
    
    @abstractmethod
    def generate_response(self, message):
        """
        Send a message to the chat interface.

        :param message: The message to be sent.
        """
        pass

    
    @abstractmethod
    def update_path(self, new_path):
        """
        Update the path for the file loader.

        :param new_path: The new path to be set.
        """
        pass
    
    @abstractmethod
    def restart_chat(self):
        """
        Restart the chat interface.
        """
        pass
    
    @abstractmethod
    def load_config_file(self):
        """
        Load the configuration file.

        :return: The configuration data as a dictionary, or None if the file does not exist.
        """
        pass
    
    @abstractmethod
    def update_config_document(self, path=None, llm_model=None, active=None, embedding_model=None):
        """
        Initialize the configuration documents with the provided parameters.

        :param path: The path to be set.
        :param llm_model: The LLM model to be set.
        :param active: Boolean indicating whether the LLM model should be activated.
        :param embedding_model: The embedding model to be set.
        """
        pass
    
