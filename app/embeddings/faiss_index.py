import faiss
import numpy as np

EMBEDDING_DIM = 384

class FaissIndex:
    def __init__(self):
        self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
        self.chunk_ids: list[int] = []

    def add(self, vector: np.ndarray, chunk_id: int):
        if vector.ndim == 1:
            vector = vector.reshape(1, -1)

        self.index.add(vector)
        self.chunk_ids.append(chunk_id)

    def search(self, vector: np.ndarray, top_k: int):
        if self.index.ntotal == 0:
            return []

        if vector.ndim == 1:
            vector = vector.reshape(1, -1)

        distances, indices = self.index.search(vector, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1:
                results.append({
                    "chunk_id": self.chunk_ids[idx],
                    "score": float(1 / (1 + dist))
                })

        return results

faiss_index = FaissIndex()
