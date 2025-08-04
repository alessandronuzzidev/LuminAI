from controller.abstract_controller import AbstractController
from model.hf_session import HFSession
#from model.session import Session

from repository.configuration_file import ConfigurationFile
from repository.embedding_models_file import EmbeddingModelsFile

from services.embeddings_service import EmbeddingsService
from services.file_indexer_worker import FileIndexWorker
from services.text_extractor_service import TextExtractorService

class ControllerGUI(AbstractController):
    def __init__(self):
        super().__init__()
        self.session = HFSession()
        self.session.start_session()
        self.config_file = ConfigurationFile()
        self.embedding_models_file = EmbeddingModelsFile()
        self.file_charger = None

    def send_message(self, message):
        """
        Send a message to the chat interface.

        :param message: The message to be sent.
        """
        answer = self.session.send_message(message)
        return answer
    
    def get_path(self):
        """
        Retrieve the path for the file loader.

        :return: The path as a string.
        """
        path = ""
        config_data = self.config_file.load_config_file()
        if config_data and "path" in config_data:
            path = config_data["path"]
        
        return path 

    def update_path(self, new_path):
        """
        Update the path for the file loader.

        :param new_path: The new path to be set.
        """
        config_data = self.config_file.load_config_file()
        config_data["path"] = new_path
        self.config_file.generate_config_file(config_data)

    def get_llm_model(self):
        """
        Retrieve the current LLM model.

        :return: The LLM model as a string.
        """
        llm_model = ""
        config_data = self.config_file.load_config_file()
        if config_data and "llm_model" in config_data:
            llm_model = config_data["llm_model"]
            
        return llm_model
    
    def update_llm_model(self, new_model):
        """
        Update the LLM model used by the controller.

        :param new_model: The new LLM model to be set.
        """
        config_data = self.config_file.load_config_file()
        config_data["llm_model"] = new_model
        self.config_file.generate_config_file(config_data)
        
    def is_llm_model_activated(self):
        """
        Check if the LLM model is activated.

        :return: True if the LLM model is activated, False otherwise.
        """
        activated = False
        config_data = self.config_file.load_config_file()
        if config_data and "llm_model_activated" in config_data:
            activated = config_data["llm_model_activated"]
        
        return activated
    
    def llm_model_change_status(self, active):
        """
        Set the activation status of the LLM model.

        :param active: Boolean indicating whether the LLM model should be activated.
        """
        config_data = self.config_file.load_config_file()
        config_data["llm_model_activated"] = active
        self.config_file.generate_config_file(config_data)
        
    def get_embedding_model(self):
        """
        Retrieve the current embedding model.

        :return: The embedding model as a string.
        """
        embedding_model = ""
        config_data = self.config_file.load_config_file()
        if config_data and "embedding_model" in config_data:
            embedding_model = config_data["embedding_model"]
        
        return embedding_model
    
    def update_embedding_model(self, new_model):
        """
        Update the embedding model used by the controller.

        :param new_model: The new embedding model to be set.
        """
        config_data = self.config_file.load_config_file()
        config_data["embedding_model"] = new_model
        self.config_file.generate_config_file(config_data)
    
    def restart_chat(self):
        """
        Restart the chat interface.
        """
        self.session.end_session()
        self.session.start_session()
        pass
    
    def load_config_file(self):
        """
        Load the configuration file.

        :return: The configuration data as a dictionary, or None if the file does not exist.
        """
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
        """
        Initialize the configuration documents with the provided parameters.

        :param path: The path to be set.
        :param llm_model: The LLM model to be set.
        :param active: Boolean indicating whether the LLM model should be activated.
        :param embedding_model: The embedding model to be set.
        """
        self.config_file.generate_config_file({
            "path": path,
            "llm_model": llm_model,
            "llm_model_activated": active,
            "embedding_model": embedding_model
        })
        
    def load_embedding_models_file(self):
        """
        Load the embedding models file.

        :return: The embedding models data as a list, or an empty list if the file does not exist.
        """
        embedding_models_data = self.embedding_models_file.load_embedding_models_file()
        if embedding_models_data:
            return embedding_models_data
        else:
            print("No embedding models file found.")
            default_embedding_models = []
            self.embedding_models_file.generate_embedding_models_file(default_embedding_models)
            return default_embedding_models
        
    def file_indexer(self):
        """
        Create Worker for subprocess of loading documents to database.
        
        :return: The object that extracts the text from different types of documents.
        """
        text_extractor_service = TextExtractorService()
        return FileIndexWorker(index_function= text_extractor_service.extract_text)