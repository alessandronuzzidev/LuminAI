from langchain_ollama import OllamaEmbeddings
import subprocess

class ParaphraseMultilingualMiniLM:
    
    def __init__(self):
        subprocess.run(["ollama", "pull", "nextfire/paraphrase-multilingual-minilm:l12-v2"], check=True)
        self.embedding_model = OllamaEmbeddings(model="nextfire/paraphrase-multilingual-minilm:l12-v2")
        
