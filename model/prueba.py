from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np

# Ruta local al modelo clonado o descargado
local_model_path = "hf_models/mxbai-embed-large-v1"

# Crear el modelo de embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name=local_model_path,
    model_kwargs={
        "trust_remote_code": True,
        "device": "cpu"
    },
    encode_kwargs={"normalize_embeddings": True}
)

# Tus frases
sentences = [
    "Él es una persona feliz",
    "Él es un humano feliz",
    "Él es un humano triste",
    "Él es un perro feliz",
    "That is a happy human"
]

# Obtener los embeddings
embeddings = embedding_model.embed_documents(sentences)

# Convertir a array de NumPy para poder hacer similitud
embeddings_np = np.array(embeddings)

# Calcular matriz de similitud coseno entre todos los pares
norms = np.linalg.norm(embeddings_np, axis=1, keepdims=True)
normalized = embeddings_np / norms
similarities = np.matmul(normalized, normalized.T)

# Mostrar resultados
print("Shape embeddings:", embeddings_np.shape)
print("Shape similarities:", similarities.shape)
print("Embeddings:\n", embeddings_np)
print("Similarity matrix:\n", similarities)
