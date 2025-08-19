from controller.abstract_controller import AbstractController

from PySide6.QtCore import QThread
from model.session_semantic_search_rag import SessionSemanticSearchRag
from model.session_semantic_search import SessionSemanticSearch
from repository.configuration_file import ConfigurationFile
from repository.embedding_models_file import EmbeddingModelsFile

import services.embeddings_lib as embedding
from services.file_indexer_worker import FileIndexWorker
from services.text_extractor_service import TextExtractorService


class ControllerGUI(AbstractController):
    def __init__(self):
        super().__init__()
        self.sessions_dict = {
            "RAG": SessionSemanticSearchRag(),
            "NOT_RAG": SessionSemanticSearch()
        }
        
        self.config_file = ConfigurationFile()
        self.embedding_models_file = EmbeddingModelsFile()
        self.file_charger = None
        configuration = self.config_file.load_config_file()
        if configuration["checkbox_rag_value"]:
            self.session = self.sessions_dict["RAG"]
        else:
            self.session = self.sessions_dict["NOT_RAG"]
        self.session.start_session()

    def generate_response(self, message):
        """
        Send a message to the chat interface.

        :param message: The message to be sent.
        """
        answer = self.session.generate_response(message)
        return answer
    
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
        if not config_data:
            self.update_config_document(path="")
            config_data = self.config_file.load_config_file()
        return config_data
        
    def update_path(self, path):
        """
        Update the path for the file loader.

        :param new_path: The new path to be set.
        """
        config_data = self.config_file.load_config_file()
        self.update_config_document(path, config_data["checkbox_rag_value"], config_data["similarity_threshold_value"])
    
    def update_config_document(self, path=None, checkbox_rag_value=True, similarity_threshold_value=0.7):
        """
        Initialize the configuration documents with the provided parameters.

        :param path: The path to be set.
        :param content_management: Content management policy.
        :param embedding_model: The embedding model to be set.
        """
        old_config = self.load_config_file()
        self.config_file.generate_config_file({
            "path": path,
            "checkbox_rag_value": checkbox_rag_value,
            "similarity_threshold_value": similarity_threshold_value,
            "embedding_model": old_config["embedding_model"],
            "llm_model": old_config["llm_model"]
        })
        new_config = self.load_config_file()
        
        if old_config["checkbox_rag_value"] != new_config["checkbox_rag_value"]:
            self.session.end_session()
            if new_config["checkbox_rag_value"]:
                self.session = self.sessions_dict["RAG"]
                self.session.start_session()
            else:
                self.session = self.sessions_dict["NOT_RAG"]
                self.session.start_session()      
        
        if path != "" and old_config["path"] != new_config["path"]:
            embedding.restart()
            return True
        
        return False
        
    def thread_function(self, update_function, progress_dialog):
        self.thread = QThread()
        self.worker = self.file_indexer()
        self.worker.moveToThread(self.thread)

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
        return FileIndexWorker(index_function= text_extractor_service.extract_and_save_text)