from langchain.vectorstores import Chroma
from langchain_core.documents import Document
from uuid import uuid4
from repository.abstract_vector_db_repository import AbstractVectorDBRepository

import os
import shutil

class ChromaRepository(AbstractVectorDBRepository):
    
    def __init__(self, embeddings=None, persist_directory="./chroma_db", collection_name="luminai_collection"):
        """
        Inicializa el repositorio usando Chroma vector DB.
        
        :param embeddings: función o modelo para obtener embeddings
        :param persist_directory: carpeta local para persistencia
        :param collection_name: nombre de la colección en Chroma
        """
        self.persist_directory = persist_directory
        self.vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        
    def add(self, page_content, metadata=None):
        """
        Añadir documento(s) a Chroma.
        """
        document = Document(
            page_content=page_content,
            metadata=metadata or {},
        )
        self.vector_store.add_documents([document], ids=[str(uuid4())])
        
    def query(self, query, top_k=10, filter=None):
        results = self.vector_store.similarity_search(
            query=query,
            k=top_k,
            filter=filter,
            # return_source_documents=True  # <-- quitar o comentar esta línea
        )
        return results
        
    def delete(self, vector_id):
        """
        Borrar vector por ID (Chroma no expone método directo, este método puede variar según versión).
        """
        # Nota: Chroma actual no tiene delete por ID en la API oficial aún
        # Podrías recrear la colección filtrando o no usar delete en local
        print("Delete no implementado en esta versión de Chroma.")
        
    def save_index(self, path=None):
        """
        Chroma guarda automáticamente en persist_directory, no se necesita método save explícito.
        """
        self.vector_store.persist()
        
    def delete_all(self):
        """
        Eliminar todos los vectores (borrar carpeta con persistencia).
        """
        self.vector_store.delete_collection()
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)


"""from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np

# Ruta local al modelo clonado o descargado
local_model_path = "hf_models/mxbai-embed-large-v1"

print("Creating HuggingFace embeddings model...")
# Crear el modelo de embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name=local_model_path,
    model_kwargs={
        "trust_remote_code": True,
        "device": "cpu"
    },
    encode_kwargs={"normalize_embeddings": True}
)
print("Model created...") 

# Crear repositorio FAISS
db = ChromaRepository(embeddings=embedding_model)

print("Creating ChromaRepository repository with embeddings...")        

print("ChromaRepository repository created successfully.")
print("Adding documents to ChromaRepository repository...")
# Example usage
db.add("Titanic fue un barco que se hundió.", metadata={"source": "test_source"})
db.add("Superman fue un superhéroe.", metadata={"source": "test_source_2"})
db.add("Batman es un rico con un traje.", metadata={"source": "test_source_3"})
db.add("Avatar es una película dirigida por James Cameron.", metadata={"source": "test_source_4"})
db.add("Langchain es una librería de alto nivel para RAG.", metadata={"source": "test_source_5"})
db.add("FAISS es una base de datos vectorial.", metadata={"source": "test_source_6"})
db.add("Alfaraz de Sayago es un pueblo en Zamora.", metadata={"source": "test_source_7"})
db.add("El Real Madrid es el club de fútbol más importante del mundo.", metadata={"source": "test_source_8"})
db.add("El judo es un arte marcial japonés.", metadata={"source": "test_source_9"})
db.add("China compite muy bien en el tenis de mesa.", metadata={"source": "test_source_10"})
db.add("Las Pleyades son una constelación asombrosa.", metadata={"source": "test_source_11"})
db.add("Esto es un ejemplo de uso de FAISS con LangChain.", metadata={"source": "test_source_12"})
print("Documents added successfully.")

print("Querying FAISS repository...")
results = db.query("Equipo de balonpié más relevante", top_k=5)
for res in results:
    print(f"* {res.page_content} [{res.metadata}]")

print("Saving FAISS index...")

db.save_index("faiss_index")
db.delete_all()"""