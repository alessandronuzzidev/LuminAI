from controller.abstract_controller import AbstractController
from model.hf_session import HFSession
from PySide6.QtCore import QThread

from repository.configuration_file import ConfigurationFile
from repository.embedding_models_file import EmbeddingModelsFile

import services.embeddings_lib as embedding
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
                "all_doc": True,
                "summarize": False,
                "most_important_entities": False,
                "embedding_model": "nomic-embed-text-v1.5"
            }
            self.config_file.generate_config_file(default_config)
            return default_config
        
    def update_path(self, path):
        config_data = self.config_file.load_config_file()
        content_management = {
            "all_doc": config_data["all_doc"], 
            "summarize": config_data["summarize"], 
            "most_important_entities": config_data["most_important_entities"]
        }
        self.update_config_document(path, content_management, config_data["embedding_model"])
    
    def update_config_document(self, path=None, content_management={"all_doc": True, "summarize": False, "most_important_entities": False}, embedding_model=None):
        """
        Initialize the configuration documents with the provided parameters.

        :param path: The path to be set.
        :param content_management: Content management policy.
        :param embedding_model: The embedding model to be set.
        """
        old_config = self.load_config_file()
        self.config_file.generate_config_file({
            "path": path,
            "all_doc": content_management["all_doc"],
            "summarize": content_management["summarize"],
            "most_important_entities": content_management["most_important_entities"],
            "embedding_model": embedding_model
        })
        new_config = self.load_config_file()
        
        if path != "" and old_config != new_config:
            embedding.restart()
            return True
        
        return False
        
    def load_content_management(self):
        config_data = self.config_file.load_config_file()
        if config_data["most_important_entities"]:
            return "most_important_entities"
        elif config_data["summarize"]:
            return "summarize"
        else:
            return "all_doc"
        
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
        
    def thread_function(self, update_function, progress_dialog):
        # Crear hilo y worker
        self.thread = QThread()
        self.worker = self.file_indexer()
        self.worker.moveToThread(self.thread)

        # Conectar señales
        self.worker.progress.connect(update_function)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(progress_dialog.close)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        
    def file_indexer(self):
        """
        Create Worker for subprocess of loading documents to database.
        
        :return: The object that extracts the text from different types of documents.
        """
        text_extractor_service = TextExtractorService()
        return FileIndexWorker(index_function= text_extractor_service.extract_text)