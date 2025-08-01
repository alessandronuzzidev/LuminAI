from services.abstract_embeddings_service import AbstractEmbeddingsService
from model.mxbai_embedding import MxbaiEmbedding
from model.nomic_embedding import NomicEmbedding
from repository.chroma_repository import ChromaRepository

import json

class EmbeddingsService(AbstractEmbeddingsService):
    def __init__(self):
        super().__init__()
        self.embedding_valid = True
        
        embedding_models = {
            "mxbai-embed-large-v1": MxbaiEmbedding,
            "nomic-embed-text-v1.5": NomicEmbedding
        }
        
        json_path = "data/config.json"
        with open(json_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        model_name = config.get("embedding_model")
        if model_name not in embedding_models:
            raise ValueError(f"Modelo de embedding no válido: {model_name}")
        
        self.embedding_model = embedding_models[model_name]()
        self.repository = ChromaRepository(
            embeddings=self.embedding_model.embedding_model)
    
    def save_documents(self, document, metadata):
        """
        Embeds a list of documents using the specified embedding model.
        
        :param documents: A list of documents to embed.
        :return: A list of embedded representations of the documents.
        """
        if not self.embedding_valid:
            raise ValueError("Modelo de embedding no válido o no inicializado correctamente.")
        if not document:
            raise ValueError("Documento erróneo.")
        if not isinstance(document, str):
            raise TypeError("El documento debe ser cadena de texto.")
        self.repository.add(page_content=document, metadata=metadata)
    
    def query_embedding(self, query):
        """
        Embeds a query and returns its embedding.
        
        :param query: The query to embed.
        :return: The embedded representation of the query.
        """
        output = []
        output.append(self.repository.query(query=query, top_k=5))
        return output