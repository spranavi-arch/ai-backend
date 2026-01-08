import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Vector dimension for this model
VECTOR_DIM = 384

# In-memory FAISS index
index = faiss.IndexFlatL2(VECTOR_DIM)

# Map FAISS position -> document_id
doc_id_map: list[int] = []

def index_document_text(document_id: int, text: str):
    if not text or not text.strip():
        raise ValueError("Document has no content to index")

    embedding = model.encode([text])
    embedding = np.array(embedding).astype("float32")

    index.add(embedding)
    doc_id_map.append(document_id)

def semantic_search(query: str, top_k: int):
    if index.ntotal == 0:
        return []

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(doc_id_map):
            results.append(doc_id_map[idx])

    return results
