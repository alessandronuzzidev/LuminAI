from collections import defaultdict

from langchain_chroma import Chroma
from langchain_core.documents import Document
from uuid import uuid4
from repository.abstract_vector_db_repository import AbstractVectorDBRepository
from langchain.text_splitter import RecursiveCharacterTextSplitter

import gc

import os
import shutil

class ChromaRepository(AbstractVectorDBRepository):
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ChromaRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self, embeddings=None, persist_directory="./chroma_db", collection_name="luminai_collection"):
        if hasattr(self, "_initialized") and self._initialized:
            return  

        self.embeddings = embeddings
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        self._initialized = True

    def add(self, page_content, metadata=None):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        
        chunks = text_splitter.split_text(page_content)
        
        self.vector_store.add_texts(
            texts=chunks,
            metadatas=[metadata] * len(chunks)
        )
        
        del chunks, page_content, metadata
        gc.collect()
        
    def query(self, query, top_k=10, filter=None):
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
        print("Delete no implementado en esta versión de Chroma.")
        
    def restart(self):
        """
        Delete all vectors from the database and reset the persistence directory.
        """
        self.vector_store.delete_collection()
        self.vector_store = None

        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )

    def as_retriever(self, score_threshold=0.7, top_k=5):
        """
        Devuelve un retriever que sólo retorna documentos por encima del threshold.
        """
        if top_k is None:
            return self.vector_store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={'score_threshold': score_threshold}
            )
        else:
            return self.vector_store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={'score_threshold': score_threshold, 'k': top_k}
            )


