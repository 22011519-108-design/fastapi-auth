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

        store.add(
            embedding,
            metadata
        )


def hybrid_search(query: str, k: int = 5):
    """
    Combine vector and BM25 retrieval using normalized scores.
    """

    # Vector search
    embedding = get_embedding(query)

    vector_results = store.search(
        embedding,
        k
    )

    # BM25 search
    keyword_results = store.keyword_search(
        query,
        k
    )


    combined = {}


    # Normalize vector scores
    if vector_results:

        max_distance = max(
            item["distance"]
            for item in vector_results
        )

        for item in vector_results:

            title = item["metadata"]["title"]

            vector_score = (
                1 -
                (item["distance"] / max_distance)
            ) if max_distance else 1


            combined[title] = {
                "metadata": item["metadata"],
                "score": 0.7 * vector_score
            }


    # Normalize BM25 scores
    if keyword_results:

        max_bm25 = max(
            item["score"]
            for item in keyword_results
        )


        for item in keyword_results:

            title = item["metadata"]["title"]

            bm25_score = (
                item["score"] / max_bm25
            ) if max_bm25 else 0


            if title in combined:

                combined[title]["score"] += (
                    0.3 * bm25_score
                )

            else:

                combined[title] = {
                    "metadata": item["metadata"],
                    "score": 0.3 * bm25_score
                }


    ranked = sorted(
        combined.values(),
        key=lambda x: x["score"],
        reverse=True
    )


    return ranked[:k]


def search_documents(
    query: str,
    k: int = 5,
    retrieval: str = "vector"
):
    """
    Search indexed document chunks.
    """

    if retrieval == "hybrid":

        return hybrid_search(
            query,
            k
        )


    embedding = get_embedding(query)

    return store.search(
        embedding,
        k
    )