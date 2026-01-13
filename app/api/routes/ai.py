from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.ask import AskRequest
from app.core.database import get_db
from app.services.search import search_chunks
from app.services.search_utils import hydrate_chunks
from app.services.llm import ask_llm

router = APIRouter()

SYSTEM_PROMPT = """
You are a factual assistant.
Answer ONLY using the provided context.
If the answer is not present, say:
"The information is not available in the document."
"""

@router.post("/ai/ask")
def ask_ai(payload: AskRequest, db: Session = Depends(get_db)):
    query = payload.query     
    k = payload.k   

    raw_results = search_chunks(query, k)
    chunks = hydrate_chunks(db, raw_results)

    if not chunks:
        return {
            "query": query,
            "answer": "The information is not available in the document.",
            "use_web": True
        }

    context = "\n\n".join(c["content"] for c in chunks)

    answer = ask_llm(
        system_prompt=SYSTEM_PROMPT,
        context=context,
        question=query
    )

    return {
        "query": query,
        "documents": chunks,
        "answer": answer,
        "use_web": False
    }
