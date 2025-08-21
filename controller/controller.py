from controller.abstract_controller import AbstractController

from PySide6.QtCore import QThread
from model.session_semantic_search_rag import SessionSemanticSearchRag
from model.session_semantic_search import SessionSemanticSearch
from repository.configuration_file import ConfigurationFile
from repository.embedding_models_file import EmbeddingModelsFile

import socket, json


class Controller(AbstractController):
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
            return True
        
        return False
        
    def get_total_documents(self) -> int:
        """
        Get the total number of documents in the specified path.
        :return: The total number of documents.
        """
        config_file = self.config_file.load_config_file()
        return len(self.list_documents(config_file["path"]))

    def list_documents(self, path: str):
        """
        List all documents in the specified path.
        :param path: The path to search for documents.
        :return: A list of document paths.
        """
        import os
        doc_list = []
        for root, _, files in os.walk(path):
            for f in files:
                doc_list.append(os.path.join(root, f))
        return doc_list

    def index_documents(self):
        """
        Index all documents in the specified path.
        :param progress_callback: Optional callback function to update progress.
        """
        config_file = self.config_file.load_config_file()
        docs = self.list_documents(config_file["path"])
        total = len(docs)
        
        for i, doc_path in enumerate(docs, start=1):
            task = {
                "src_path": doc_path,
                "action": "created"
            }
            with socket.socket() as s:
                s.connect(("127.0.0.1", 65432))
                s.send(json.dumps(task).encode())
                response = s.recv(1024)
        return 
    
    def cancel_indexing(self):
        """
        Cancel the indexing process.
        """
        s = socket.socket()
        s.connect(("127.0.0.1", 65432))
        task = {"cancel": True,}
        s.send(json.dumps(task).encode())
        response = s.recv(1024)
        s.close()
        
    def get_progress(self):
        """
        Get the progress of the indexing process.
        :return: A tuple containing the number of completed tasks and the total number of tasks.
        """
        s = socket.socket()
        s.connect(("127.0.0.1", 65432))
        task = {"progress": True,}
        s.send(json.dumps(task).encode())
        response = s.recv(1024)
        s.close()
        data = json.loads(response.decode())
        
        if "completed" in data and "total" in data:
            return data["completed"], data["total"]
        return None, None