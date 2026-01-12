from app.ai.llm import client, DEPLOYMENT

def classify_intent(state: dict) -> dict:
    prompt = f"""
You are an intent classifier.

Classify the user query into ONE category:
- search
- summarize
- question

User query:
{state["query"]}

Return ONLY the category name.
"""


    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    intent = response.choices[0].message.content.strip().lower()
    state["intent"] = intent
    return state


