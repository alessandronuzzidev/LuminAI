from abc import ABC, abstractmethod

class AbstractEmbeddingsService(ABC):

    @abstractmethod
    def save_documents(self, documents):
        """
        Embeds a list of documents using the specified embedding model.
        
        :param documents: A list of documents to embed.
        :return: A list of embedded representations of the documents.
        """
        raise NotImplementedError("This method should be overridden by subclasses")
    
    @abstractmethod
    def query_embedding(self, query):
        """
        Embeds a query and returns its embedding.
        
        :param query: The query to embed.
        :return: The embedded representation of the query.
        """
        raise NotImplementedError("This method should be overridden by subclasses")
    