from app.modules.rag.chunking import chunk_text
from app.modules.rag.embeddings import get_embedding
from app.modules.rag.vector_store import VectorStore

store = VectorStore()


def index_document(title: str, text: str):
    """
    Split a document into chunks, generate embeddings,
    and store them in FAISS.
    """

    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):

        embedding = get_embedding(chunk)

        metadata = {
            "title": title,
            "chunk_number": i + 1,
            "text": chunk,
        }

        store.add(embedding, metadata)


def search_documents(query: str, k: int = 5):
    """
    Search indexed document chunks.
    """

    embedding = get_embedding(query)

    return store.search(embedding, k)