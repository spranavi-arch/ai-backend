import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
VECTOR_DIM = 384

index = faiss.IndexFlatL2(VECTOR_DIM)
doc_id_map: list[int] = []


def index_document_text(document_id: int, text: str):
    if not text or not text.strip():
        raise ValueError("Document has no content to index")

    embedding = model.encode([text])
    embedding = np.array(embedding).astype("float32")

    index.add(embedding)
    doc_id_map.append(document_id)


def search_documents(query: str, k: int):
    if index.ntotal == 0:
        return []

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx < len(doc_id_map):
            score = float(1 / (1 + dist))  # Convert distance → similarity
            results.append({
                "document_id": doc_id_map[idx],
                "score": round(score, 4)
            })

    return results
