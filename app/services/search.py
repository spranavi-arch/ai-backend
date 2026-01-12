from sentence_transformers import SentenceTransformer
import numpy as np
from sqlalchemy.orm import Session

from app.embeddings.faiss_index import faiss_index
from app.services.chunking import chunk_text
from app.models.document_chunk import DocumentChunk

model = SentenceTransformer("all-MiniLM-L6-v2")


def index_document_text(
    db: Session,
    document_id: int,
    text: str
):
    chunks = chunk_text(text)

    for chunk in chunks:
        db_chunk = DocumentChunk(
            document_id=document_id,
            content=chunk
        )
        db.add(db_chunk)
        db.flush()  # get chunk id

        embedding = model.encode(chunk)
        embedding = np.array(embedding).astype("float32")

        faiss_index.add(embedding, db_chunk.id)

    db.commit()


def search_chunks(query: str, k: int):
    query_embedding = model.encode(query)
    query_embedding = np.array(query_embedding).astype("float32")

    return faiss_index.search(query_embedding, top_k=k)
