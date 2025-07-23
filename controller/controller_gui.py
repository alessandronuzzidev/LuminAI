from controller.abstract_controller import AbstractController
from model.session import Session

from services.configuration_file import ConfigurationFile

class ControllerGUI(AbstractController):
    def __init__(self):
        super().__init__()
        self.session = Session()
        self.session.start_session()
        self.config_file = ConfigurationFile()

    def send_message_to_llm(self, message):
        # print(f"Sending message to LLM: {message}")
        answer = self.session.send_message(message)
        # print(f"Received answer from LLM: {answer}")
        return answer
    
    def get_path(self):
        path = ""
        config_data = self.config_file.load_config_file()
        if config_data and "path" in config_data:
            path = config_data["path"]
        
        return path 
    
    def init_charge_documents(self, path=None, model=None):
        self.config_file.generate_config_file({
            "path": path,
            "model": model
        })

    def update_path(self, new_path):
        pass

    def update_model(self, new_model):
        pass
    
    def restart_chat(self):
        self.session.end_session()
        self.session.start_session()
        pass