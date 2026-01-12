from app.services.search import search_documents

def retrieve_documents(state: dict) -> dict:
    results = search_documents(
        query=state["query"],
        k=state.get("k", 5)
    )

    state["documents"] = results
    return state
