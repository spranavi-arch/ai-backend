import faiss
import numpy as np

EMBEDDING_DIM = 384  # MiniLM

class FaissIndex:
    def __init__(self):
        self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
        self.document_ids = []

    def add(self, vector: np.ndarray, document_id: int):
        self.index.add(vector)
        self.document_ids.append(document_id)

    def search(self, vector: np.ndarray, top_k: int):
        distances, indices = self.index.search(vector, top_k)
        results = []
        for idx in indices[0]:
            if idx < len(self.document_ids):
                results.append(self.document_ids[idx])
        return results

faiss_index = FaissIndex()
