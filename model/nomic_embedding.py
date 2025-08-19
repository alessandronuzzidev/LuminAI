from langchain_ollama import OllamaEmbeddings
import subprocess

class NomicEmbedding:
    
    def __init__(self):
        subprocess.run(["ollama", "pull", "nomic-embed-text"], 
                       check=True,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        self.embedding_model = OllamaEmbeddings(model="nomic-embed-text")
       