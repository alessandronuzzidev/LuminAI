import os
from .llama_llm import LlamaLLM
from repository.configuration_file import ConfigurationFile
import services.embeddings_lib as embedding

from model.abstract_model_session import AbstractModelSession

class SessionSemanticSearch(AbstractModelSession):
    """
    Session class that extends AbstractSession for managing a chat session.
    """
    
    def __init__(self):
        super().__init__()
        self.llm = LlamaLLM()
        self.messages = []
        
    def start_session(self):
        """
        Start a new session.
        """
        self.session_available = True
    
    def generate_response(self, message):
        """
        Send a message in the current session.

        :param message: The message to be sent.
        :return: The response from the LLM.
        """
        top_k = 10
        self.messages.append(message)
        message_normalized = self.llm.query_normalizer(message)
        config_file_repo = ConfigurationFile()
        config_file = config_file_repo.load_config_file()
        files_paths = embedding.query_embedding(message_normalized, config_file["similarity_threshold_value"], top_k=top_k)
        if not files_paths:
            response_text = "No se encontraron documentos relevantes. Prueba a bajar el nivel de similitud en la confoguración."
            self.messages.append(response_text)
            return response_text
        response_text = "Los documentos más similares son:\n"
        for file_path in files_paths:
            _, filename = os.path.split(file_path)
            response_text += f"- <b>{filename}</b> <i>({file_path})</i>\n"

        self.messages.append(response_text)

        return response_text

    def get_messages(self):
        """
        Get the messages from the current session.

        :return: A list of messages in the session.
        """
        return self.messages
    
    def end_session(self):
        """
        End the current session.
        """
        self.messages = []
        self.session_available = False
    