from controller.abstract_controller import AbstractController
#from model.hf_session import HFSession
from model.session import Session

from repository.configuration_file import ConfigurationFile
from repository.embedding_models_file import EmbeddingModelsFile

from services.file_charger import FileCharger

class ControllerGUI(AbstractController):
    def __init__(self):
        super().__init__()
        self.session = Session()
        self.session.start_session()
        self.config_file = ConfigurationFile()
        self.embedding_models_file = EmbeddingModelsFile()
        self.file_charger = FileCharger()

    def send_message(self, message):
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

    def update_path(self, new_path):
        config_data = self.config_file.load_config_file()
        config_data["path"] = new_path
        self.config_file.generate_config_file(config_data)

    def get_llm_model(self):
        llm_model = ""
        config_data = self.config_file.load_config_file()
        if config_data and "llm_model" in config_data:
            llm_model = config_data["llm_model"]
            
        return llm_model
    
    def update_llm_model(self, new_model):
        config_data = self.config_file.load_config_file()
        config_data["llm_model"] = new_model
        self.config_file.generate_config_file(config_data)
        
    def is_llm_model_activated(self):
        activated = False
        config_data = self.config_file.load_config_file()
        if config_data and "llm_model_activated" in config_data:
            activated = config_data["llm_model_activated"]
        
        return activated
    
    def llm_model_change_status(self, active):
        config_data = self.config_file.load_config_file()
        config_data["llm_model_activated"] = active
        self.config_file.generate_config_file(config_data)
        
    def get_embedding_model(self):
        embedding_model = ""
        config_data = self.config_file.load_config_file()
        if config_data and "embedding_model" in config_data:
            embedding_model = config_data["embedding_model"]
        
        return embedding_model
    
    def update_embedding_model(self, new_model):
        config_data = self.config_file.load_config_file()
        config_data["embedding_model"] = new_model
        self.config_file.generate_config_file(config_data)
    
    def restart_chat(self):
        self.session.end_session()
        self.session.start_session()
        pass
    
    def load_config_file(self):
        config_data = self.config_file.load_config_file()
        if config_data:
            return config_data
        else:
            print("No configuration file found, generating default configuration.")
            default_config = {
                "path": "",
                "llm_model": "",
                "llm_model_activated": False,
                "embedding_model": ""
            }
            self.config_file.generate_config_file(default_config)
            return default_config
    
    def update_config_document(self, path=None, llm_model=None, active=None, embedding_model=None):
        self.config_file.generate_config_file({
            "path": path,
            "llm_model": llm_model,
            "llm_model_activated": active,
            "embedding_model": embedding_model
        })
        
    def load_embedding_models_file(self):
        embedding_models_data = self.embedding_models_file.load_embedding_models_file()
        if embedding_models_data:
            return embedding_models_data
        else:
            print("No embedding models file found.")
            default_embedding_models = []
            self.embedding_models_file.generate_embedding_models_file(default_embedding_models)
            return default_embedding_models
        
    def file_retrieval(self):
        self.file_charger.execute()