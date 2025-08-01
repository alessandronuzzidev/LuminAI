from langchain_huggingface import HuggingFaceEmbeddings

class NomicEmbedding:
    """
    Nomic Embedding class for generating embeddings using the Nomic API.
    """

    def __init__(self, path="hf_models/nomic-embed-text-v1.5"):
        """
        Initialize the NomicEmbedding with the provided API key and model.
        """
        super().__init__()
        self.path = path
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=self.path,
            model_kwargs={
                "trust_remote_code": True,
                "device": "cpu"
            },
            encode_kwargs={"normalize_embeddings": True}
        )
       