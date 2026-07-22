from sentence_transformers import SentenceTransformer

# Load the embedding model once when the application starts
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str) -> list[float]:
    """
    Convert a text string into a vector embedding.
    """
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()