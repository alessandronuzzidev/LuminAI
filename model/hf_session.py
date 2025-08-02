from langchain.schema import SystemMessage, HumanMessage
from services.embeddings_service import EmbeddingsService

from model.abstract_model_session import AbstractModelSession

class HFSession(AbstractModelSession):
    
    def __init__(self):
        super().__init__()
        self.embedding_service = EmbeddingsService()
        self.messages = []
        
    def start_session(self):
        self.session_available = True
        print("Session started.")
    
    def send_message(self, message):
        top_k = 5
        self.messages.append(message)
        answer = self.embedding_service.query_embedding(message, top_k)
        response_text = "Los documentos más similares son:\n"
        response_text += "\n".join(f"- {doc}" for doc in answer)

        self.messages.append(response_text)

        return response_text

    def get_messages(self):
        return self.messages
    
    def end_session(self):
        self.messages = None
        self.session_available = False
        print("Session ended.")
        print("Resources cleared.")
    