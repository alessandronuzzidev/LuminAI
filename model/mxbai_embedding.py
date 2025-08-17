from langchain_ollama import OllamaEmbeddings
import subprocess

class MxbaiEmbedding:
    
    def __init__(self):
        subprocess.run(["ollama", "pull", "mxbai-embed-large"], check=True)
        self.embedding_model = OllamaEmbeddings(model="mxbai-embed-large")