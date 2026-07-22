from app.modules.rag.evaluation_data import EVAL_SET
from app.modules.rag.services import search_documents


def run_evaluation(
    top_k=3,
    chunking="fixed",
    chunk_size=100,
    overlap=20,
    reranking=False,
    retrieval="vector",
):
    """
    Evaluate retrieval configurations.
    """

    print("\n" + "=" * 70)
    print("CONFIGURATION")
    print("=" * 70)
    print(f"Chunking Strategy : {chunking}")
    print(f"Chunk Size        : {chunk_size}")
    print(f"Overlap           : {overlap}")
    print(f"Top K             : {top_k}")
    print(f"Re-ranking        : {reranking}")
    print(f"Retrieval         : {retrieval}")
    print("=" * 70)

    hits = 0

    for item in EVAL_SET:

        question = item["question"]
        expected = item["expected"]

        retrieved = search_documents(question, k=top_k)

        retrieved_titles = [
            r["metadata"]["title"]
            for r in retrieved
        ]

        hit = expected in retrieved_titles

        if hit:
            hits += 1

        print("\nQuestion :", question)
        print("Expected :", expected)
        print("Retrieved Titles:")

        for i, r in enumerate(retrieved, start=1):

            print(
                f"{i}. {r['metadata']['title']} "
                f"(distance={r['distance']:.4f})"
            )

        print("Hit :", hit)

    print("\nOverall Hit Rate:", f"{hits}/{len(EVAL_SET)}")


if __name__ == "__main__":

    configurations = [

        {
            "chunking": "fixed",
            "chunk_size": 100,
            "overlap": 20,
            "top_k": 3,
            "reranking": False,
            "retrieval": "vector",
        },

        {
            "chunking": "fixed",
            "chunk_size": 150,
            "overlap": 30,
            "top_k": 5,
            "reranking": False,
            "retrieval": "vector",
        },

        {
            "chunking": "semantic",
            "chunk_size": 150,
            "overlap": 30,
            "top_k": 5,
            "reranking": True,
            "retrieval": "hybrid",
        },

    ]

    for config in configurations:

        run_evaluation(
            top_k=config["top_k"],
            chunking=config["chunking"],
            chunk_size=config["chunk_size"],
            overlap=config["overlap"],
            reranking=config["reranking"],
            retrieval=config["retrieval"],
        )