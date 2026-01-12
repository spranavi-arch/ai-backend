from langgraph.graph import StateGraph
from app.ai.state import AgentState
from app.ai.nodes.intent import classify_intent
from app.ai.nodes.retrieve import retrieve_chunks
from app.ai.nodes.decide import decide_source
from app.ai.nodes.answer import answer_from_chunks
from app.ai.nodes.summarize import summarize_chunks
from app.ai.nodes.web import web_search

graph = StateGraph(AgentState)

graph.add_node("intent", classify_intent)
graph.add_node("decide", decide_source)
graph.add_node("retrieve", retrieve_chunks)
graph.add_node("answer", answer_from_chunks)
graph.add_node("summarize", summarize_chunks)

graph.add_node("web", web_search)

graph.set_entry_point("intent")

graph.add_conditional_edges(
    "intent",
    lambda s: s["intent"],
    {
        "summarize": "retrieve",
        "question": "retrieve",
        "search": "retrieve",
    }
)

graph.add_conditional_edges(
    "retrieve",
    lambda s: s["intent"],
    {
        "summarize": "summarize",
        "question": "decide",
        "search": "decide",
    }
)


graph.add_conditional_edges(
    "decide",
    lambda s: s["use_web"],
    {
        True: "web",
        False: "answer",
    }
)

graph.add_edge("answer", "__end__")
graph.add_edge("summarize", "__end__")
graph.add_edge("web", "__end__")

agent = graph.compile()
