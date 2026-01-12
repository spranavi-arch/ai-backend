# app/ai/nodes/retrieve.py
from app.ai.state import AgentState
from app.services.search import search_chunks

def retrieve_chunks(state: AgentState):
    chunks = search_chunks(
        query=state["query"],
        k=state.get("k", 5)
    )
    state["chunks"] = chunks
    return state
