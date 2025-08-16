import services.embeddings_lib as embedding

from model.abstract_model_session import AbstractModelSession

class HFSession(AbstractModelSession):
    
    def __init__(self):
        super().__init__()
        self.messages = []
        
    def start_session(self):
        """
        Start a new session.
        """
        self.session_available = True
        print("Session started.")
    
    def generate_response(self, message):
        """
        Send a message in the current session.

        :param message: The message to be sent.
        :return: The response from the LLM.
        """
        top_k = 5
        self.messages.append(message)
        answer = embedding.query_embedding(message, top_k)
        response_text = "Los documentos más similares son:\n"
        response_text += "\n".join(f"- {doc}" for doc in answer)

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
        print("Session ended.")
        print("Resources cleared.")
    