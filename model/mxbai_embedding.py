from langchain_huggingface import HuggingFaceEmbeddings

class MxbaiEmbedding:
    
    def __init__(self, path="hf_models/mxbai-embed-large-v1"):
        self.path = path
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=self.path,
            model_kwargs={
                "trust_remote_code": True,
                "device": "cpu"
            },
            encode_kwargs={"normalize_embeddings": True}
        )