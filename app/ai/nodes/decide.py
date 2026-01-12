# app/ai/nodes/decide.py
from app.ai.state import AgentState

MIN_SCORE = 0.35
MIN_CHUNKS = 1

def decide_source(state: AgentState):
    chunks = state.get("chunks", [])

    # No chunks → web
    if not chunks:
        state["use_web"] = True
        return state

    high_conf_chunks = [c for c in chunks if c["score"] >= MIN_SCORE]

    # Not enough confident chunks → web
    if len(high_conf_chunks) < MIN_CHUNKS:
        state["use_web"] = True
    else:
        state["use_web"] = False

    return state
