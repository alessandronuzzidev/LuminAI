from abc import ABC, abstractmethod

class AbstractVectorDBRepository(ABC):
    """
    Abstract base class for vector databases.
    """

    @abstractmethod
    def add(self, vector, metadata=None):
        """
        Add a vector to the database.
        
        :param vector: The vector to add.
        :param metadata: Optional metadata associated with the vector.
        """
        pass

    @abstractmethod
    def query(self, vector, top_k=10):
        """
        Query the database for the nearest vectors to the given vector.
        
        :param vector: The vector to query against.
        :param top_k: The number of nearest vectors to return.
        :return: A list of tuples containing the nearest vectors and their metadata.
        """
        pass
    
    @abstractmethod
    def delete(self, vector_id):
        """
        Delete a vector from the database by its ID.
        
        :param vector_id: The ID of the vector to delete.
        """
        pass
    
    @abstractmethod
    def delete_all(self):
        """
        Delete all vectors from the database.
        """
        pass