import faiss
import numpy as np
import pickle
from pathlib import Path

from rank_bm25 import BM25Okapi


STORAGE_DIR = Path("storage")

INDEX_PATH = STORAGE_DIR / "faiss.index"
METADATA_PATH = STORAGE_DIR / "metadata.pkl"


STORAGE_DIR.mkdir(exist_ok=True)


class VectorStore:

    def __init__(self, dimension: int = 384):

        self.dimension = dimension

        if INDEX_PATH.exists():

            self.index = faiss.read_index(
                str(INDEX_PATH)
            )

            with open(METADATA_PATH, "rb") as f:
                self.metadata = pickle.load(f)

        else:

            self.index = faiss.IndexFlatL2(
                dimension
            )

            self.metadata = []


        # Build BM25 index
        self.build_bm25()


    def build_bm25(self):

        """
        Creates BM25 keyword search index.
        """

        documents = []

        for item in self.metadata:

            text = item.get(
                "text",
                ""
            )

            documents.append(
                text.split()
            )


        if documents:

            self.bm25 = BM25Okapi(
                documents
            )

        else:

            self.bm25 = None



    def save(self):

        faiss.write_index(
            self.index,
            str(INDEX_PATH)
        )


        with open(
            METADATA_PATH,
            "wb"
        ) as f:

            pickle.dump(
                self.metadata,
                f
            )


    def add(
        self,
        embedding,
        metadata
    ):

        vector = np.array(
            [embedding],
            dtype="float32"
        )


        self.index.add(
            vector
        )


        self.metadata.append(
            metadata
        )


        self.save()

        self.build_bm25()



    def search(
        self,
        embedding,
        k=5
    ):

        vector = np.array(
            [embedding],
            dtype="float32"
        )


        distances, indices = self.index.search(
            vector,
            k
        )


        results = []


        for distance, idx in zip(
            distances[0],
            indices[0]
        ):

            if idx == -1:
                continue


            results.append(
                {
                    "distance": float(distance),
                    "metadata": self.metadata[idx],
                }
            )


        return results



    def keyword_search(
        self,
        query,
        k=5
    ):

        """
        BM25 keyword retrieval.
        """


        if not self.bm25:
            return []


        scores = self.bm25.get_scores(
            query.split()
        )


        ranked = np.argsort(
            scores
        )[::-1][:k]


        results = []


        for idx in ranked:

            results.append(
                {
                    "score": float(scores[idx]),
                    "metadata": self.metadata[idx]
                }
            )


        return results