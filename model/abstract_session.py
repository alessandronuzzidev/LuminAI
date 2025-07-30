from abc import ABC, abstractmethod
from pathlib import Path



class AbstractSession(ABC):
    """
    Abstract class for managing sessions in the application.
    This class should be extended by any session management implementation.
    """
    def __init__(self):
        self.session_available = False
        self.messages = []

    @abstractmethod
    def start_session(self):
        """
        Start a new session.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    @abstractmethod
    def send_message(self, message):
        """
        Send a message in the current session.

        :param message: The message to be sent.
        :return: The response from the LLM.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    @abstractmethod
    def get_messages(self):
        """
        Get the messages from the current session.

        :return: A list of messages in the session.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def end_session(self):
        """
        End the current session.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")