import faiss
import numpy as np
import pickle
from pathlib import Path


# Storage paths
STORAGE_DIR = Path("storage")
INDEX_PATH = STORAGE_DIR / "faiss.index"
METADATA_PATH = STORAGE_DIR / "metadata.pkl"

# Ensure storage folder exists
STORAGE_DIR.mkdir(exist_ok=True)


class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension

        # Create a new FAISS index
        if INDEX_PATH.exists():
            self.index = faiss.read_index(str(INDEX_PATH))

            # Load metadata
            with open(METADATA_PATH, "rb") as f:
                self.metadata = pickle.load(f)

        else:
            self.index = faiss.IndexFlatL2(dimension)
            self.metadata = []

    def save(self):
        """Save index and metadata to disk."""
        faiss.write_index(self.index, str(INDEX_PATH))

        with open(METADATA_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    def add(self, embedding, metadata):
        """Add a vector and its metadata."""

        vector = np.array([embedding], dtype="float32")

        self.index.add(vector)

        self.metadata.append(metadata)

        self.save()

    def search(self, embedding, k=5):
        """Search for similar vectors."""

        vector = np.array([embedding], dtype="float32")

        distances, indices = self.index.search(vector, k)

        results = []

        for distance, idx in zip(distances[0], indices[0]):

            if idx == -1:
                continue

            results.append(
                {
                    "distance": float(distance),
                    "metadata": self.metadata[idx],
                }
            )

        return results