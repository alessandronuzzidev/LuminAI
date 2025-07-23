from model.abstract_session import AbstractSession
from langchain.schema import SystemMessage, HumanMessage
import subprocess
import requests
import signal

class Session(AbstractSession):
    """
    Session class that extends AbstractSession for managing a chat session.
    It uses the ChatOllama model for generating responses and OllamaEmbeddings for embeddings.
    """
    
    def __init__(self):
        super().__init__()
        
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
    
    def stop_ollama(ollama_process):
        try:
            ollama_process.send_signal(signal.SIGINT)
            ollama_process.wait(timeout=5)
            print("Ollama detenido correctamente.")
        except Exception as e:
            print(f"Error al detener Ollama: {e}")
        
    def start_session(self):
        """
        Start a new session by clearing previous messages.
        """
        self.session_available = True
        self.start_ollama_server()
        self.messages = [
            SystemMessage(content="Eres un asistente que ayuda a los usuarios del sistema a encontrar los " +
            "archivos en los que se habla del tema que se le indica. El usuario te dirá el tema " + 
            "y tú le dirás en qué archivos del sistema se habla de ese tema. Si no se habla de ese tema en " + 
            "ningún archivo local, entonces le dirás que no se habla de ese tema en ningún archivo. " +
            "Es necesario que indiques la ruta del archivo especificado en el metadata, en path. " + 
            "Presentalo como bullet points. Debes ser escueto para que seas lo más rápido posible. " +
            "Por último, no uses markdown, sino HTML. Por ejemplo, si usas ** para negrita, usa <b> en su lugar. " +
            "Si usas * para cursiva, usa <i> en su lugar. Si usas ` para código, usa <code> en su lugar. " +
            "Si usas [texto](enlace), usa <a href='enlace'>texto</a> en su lugar. ")
        ]
        print("Session started.")
        
    def send_message(self, message):
        """
        Send a message in the current session and get a response from the LLM.

        :param message: The message to be sent.
        :return: The response from the LLM.
        """
        self.messages.append(HumanMessage(content=message))
        response = self.llm.invoke(self.messages)
        self.messages.append(response)
        return response.content
    
    def get_messages(self):
        """
        Get the messages from the current session.

        :return: A list of messages in the session.
        """
        return self.messages
    
    def end_session(self):
        """
        End the current session by clearing messages.
        """
        self.messages = None
        self.session_available = False
        print("Session ended.")
        print("Resources cleared.")