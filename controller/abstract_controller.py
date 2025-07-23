from abc import ABC, abstractmethod
from pathlib import Path

class AbstractController(ABC):
    
    @abstractmethod
    def send_message_to_llm(self, message):
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
    def update_model(self, new_model):
        """
        Update the model used by the controller.

        :param new_model: The new model to be set.
        """
        pass
    
    @abstractmethod
    def restart_chat(self):
        """
        Restart the chat interface.
        """
        pass