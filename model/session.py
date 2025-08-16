import subprocess
import requests
import services.embeddings_lib as embedding
from .paraphrase_multilingual_MiniLM_L12_v2 import ParaphraseMultilingualMiniLM
from .llama_llm import LlamaLLM
from model.abstract_model_session import AbstractModelSession

class Session(AbstractModelSession):
    """
    Session class that extends AbstractSession for managing a chat session.
    It uses the ChatOllama model for generating responses and OllamaEmbeddings for embeddings.
    """
    
    def __init__(self):
        super().__init__()
        self.embedding_class = ParaphraseMultilingualMiniLM()
        self.llm = LlamaLLM()

        
    def is_ollama_running(self):
        try:
            response = requests.get("http://localhost:11434")
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    def start_ollama_server(self):
        if self.is_ollama_running():
            print("Ollama ya está en ejecución.")
            return

        try:
            subprocess.Popen(["ollama", "serve"])
            print("Ollama se ha arrancado correctamente.")
        except FileNotFoundError:
            print("Ollama no está instalado o no está en el PATH.")
        except Exception as e:
            print(f"Error al arrancar Ollama: {e}")
        
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
        top_k = 3
        message_normalized = self.llm.query_normalizer(message)
        files_paths = embedding.query_embedding(message_normalized, top_k)
        answer  = self.llm.generate_response(message_normalized, files_paths)
        
        return answer

    
    def get_messages(self):
        """
        Get the messages from the current session.

        :return: A list of messages in the session.
        """
        return self.llm.messages
    
    def end_session(self):
        """
        End the current session.
        """
        self.session_available = False
        self.llm.reset()