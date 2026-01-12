from app.models.document_chunk import DocumentChunk

def hydrate_chunks(db, results):
    chunks = []

    for r in results:
        chunk = db.query(DocumentChunk).get(r["chunk_id"])
        if chunk:
            chunks.append({
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "content": chunk.content,
                "score": r["score"]
            })

    return sorted(chunks, key=lambda x: x["score"], reverse=True)
