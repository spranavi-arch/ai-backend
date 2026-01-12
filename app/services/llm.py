from openai import AzureOpenAI
import os
from app.ai.llm import client, DEPLOYMENT

def ask_llm(system_prompt: str, context: str, question: str) -> str:
    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()
