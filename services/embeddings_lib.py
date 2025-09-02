from collections import defaultdict
from model.nomic_embedding import NomicEmbedding
from repository.chroma_repository import ChromaRepository

import json

from repository.sqlite_repository import SQLiteRepository



_vector_repository = None
_persist_directory = "./chroma_db"

def initialize_repository(embedding_model):
    global _vector_repository
    if _vector_repository is None:
        _vector_repository = ChromaRepository(embeddings=embedding_model, persist_directory=_persist_directory)
    return _vector_repository

def get_repository():
    global _vector_repository
    if _vector_repository is None:
        return None
    return _vector_repository

def save_documents(document, metadata):
    """
    Embeds a list of documents using the specified embedding model.
    
    :param documents: A list of documents to embed.
    :return: A list of embedded representations of the documents.
    """
    if not document:
        raise ValueError("Documento erróneo.")
    if not isinstance(document, str):
        raise TypeError("El documento debe ser cadena de texto.")
    repository = get_repository()
    ids = repository.add(page_content=document, metadata=metadata)
    
    sqlite_repo = SQLiteRepository()
    sqlite_repo.insert_index(metadata["path"], ids)
    sqlite_repo.close()
    
def delete_by_file_path(file_path):
    """
    Deletes all vectors associated with a specific file path.
    
    :param file_path: The path of the file whose vectors are to be deleted.
    """
    repository = get_repository()
    if repository is None:
        return []
    
    sqlite_repo = SQLiteRepository()
    ids = sqlite_repo.delete_by_file_path(file_path)
    sqlite_repo.close()
    
    for vector_id in ids:
        repository.delete(vector_id)

def query_embedding(query, threshold=0.7, top_k=None):
    """
    Embeds a query and returns its embedding.
    
    :param query: The query to embed.
    :return: The embedded representation of the query.
    """
    repository = get_repository()

    retriever = repository.as_retriever(score_threshold=threshold, top_k=top_k)
    
    results = retriever.invoke(query)

    output = set()
    for doc in results:
        if hasattr(doc, "metadata") and "path" in doc.metadata:
            output.add(doc.metadata["path"])
        else:
            output.add("Ruta no disponible")

    return list(output)

def create_database():
    """
    Create vector database.
    """
    embedding_models = {
        "nomic-embed-text": NomicEmbedding,
    }
    
    with open("data/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    model_name = config.get("embedding_model")
    if model_name not in embedding_models:
        raise ValueError(f"Modelo de embedding no válido: {model_name}")
    
    embedding_model = embedding_models[model_name]()
    initialize_repository(embedding_model.embedding_model)
    
def restart():
    """
    Delete vector database.
    """
    repository = get_repository()
    if repository != None:
        repository.restart()
        sqlite_repo = SQLiteRepository()
        sqlite_repo.delete_all()
        sqlite_repo.close()
        
        