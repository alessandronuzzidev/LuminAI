import subprocess
import requests
import socket, json
from .llama_llm import LlamaLLM
from model.abstract_model_session import AbstractModelSession
from repository.configuration_file import ConfigurationFile

class SessionSemanticSearchRag(AbstractModelSession):
    """
    Session class that extends AbstractSession for managing a chat session.
    It uses the ChatOllama model for generating responses and OllamaEmbeddings for embeddings.
    """
    
    def __init__(self):
        super().__init__()
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
        Send a message in the current session using a socket.
        Reads the full response even if es más grande de 1024 bytes (opción C).
        """
        top_k = 5
        message_normalized = self.llm.query_normalizer(message)
        
        config_file_repo = ConfigurationFile()
        config_file = config_file_repo.load_config_file()
        
        s = socket.socket()
        s.connect(("127.0.0.1", 65432))
        
        task = {
            "search": True,
            "message": message_normalized,
            "similarity_threshold": config_file["similarity_threshold_value"],
            "top_k": top_k
        }
        
        s.sendall(json.dumps(task).encode())

        buffer = b""
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            buffer += chunk
        
        s.close()
        
        try:
            data = json.loads(buffer.decode())
        except json.JSONDecodeError:
            return "Error: la respuesta del servidor no es válida."
        
        files_paths = data.get("results", [])

        answer = self.llm.generate_response(message_normalized, files_paths)
        
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