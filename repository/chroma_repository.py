from collections import defaultdict
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from uuid import uuid4
from repository.abstract_vector_db_repository import AbstractVectorDBRepository
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os
import shutil

class ChromaRepository(AbstractVectorDBRepository):
    
    def __init__(self, embeddings=None, persist_directory="./chroma_db", collection_name="luminai_collection"):
        self.persist_directory = persist_directory
        self.vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        
    def add(self, page_content, metadata=None):
        """
        Add a vector to the database.
        
        :param vector: The vector to add.
        :param metadata: Optional metadata associated with the vector.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        
        chunks = text_splitter.split_text(page_content)
        
        self.vector_store.add_texts(
            texts=chunks,
            metadatas=[metadata] * len(chunks)
        )
        self.vector_store.persist()
        
        del chunks, page_content, metadata
        import gc
        gc.collect()
        
    def query(self, query, top_k=10, filter=None):
        """
        Query the database for the nearest vectors to the given vector.
        
        :param vector: The vector to query against.
        :param top_k: The number of nearest vectors to return.
        :return: A list of tuples containing the nearest vectors and their metadata.
        """
        docs = self.vector_store.similarity_search_with_score(
            query=query,
            k=top_k,
            filter=filter,
        )

        grouped = defaultdict(list)
    
        for doc, score in docs:
            doc_id = doc.metadata["path"]
            grouped[doc_id].append((doc, score))

        results = []
        
        for doc_id, doc_scored in grouped.items():
            best_doc = sorted(doc_scored, key=lambda x: x[1])[0][0]
            results.append(best_doc)
        
        return results
        
    def delete(self, vector_id):
        """
        Delete a vector from the database by its ID.
        
        :param vector_id: The ID of the vector to delete.
        """
        print("Delete no implementado en esta versión de Chroma.")
        
    def delete_all(self):
        """
        Delete all vectors from the database.
        """
        self.vector_store.delete_collection()
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
