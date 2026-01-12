from app.ai.state import AgentState


def web_search(state: AgentState):
    # Placeholder (no real internet yet)
    state["answer"] = (
        "Information not found in uploaded documents. "
        "Web search fallback triggered."
    )
    return state
