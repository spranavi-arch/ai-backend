# app/ai/nodes/summarize.py
from app.ai.state import AgentState
from app.ai.llm import client, DEPLOYMENT

def summarize_chunks(state: AgentState):
    text = "\n\n".join(c["content"] for c in state["chunks"])

    prompt = f"""
Summarize the following content clearly and concisely:

{text}
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    state["answer"] = response.choices[0].message.content
    return state
