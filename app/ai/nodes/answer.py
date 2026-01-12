# app/ai/nodes/answer.py
from app.ai.state import AgentState
from app.ai.llm import client, DEPLOYMENT

def answer_from_chunks(state: AgentState):
    if state.get("use_web"):
        state["answer"] = (
            "Information is not available in uploaded documents. "
            "Web search fallback required."
        )
        return state

    context = "\n\n".join(
        f"Chunk {c['chunk_id']}:\n{c['content']}"
        for c in state["chunks"]
        if c["score"] >= 0.35
    )

    if not context.strip():
        state["answer"] = (
            "Information is not available in uploaded documents. "
            "Web search fallback required."
        )
        return state

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{state['query']}
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    state["answer"] = response.choices[0].message.content
    return state

