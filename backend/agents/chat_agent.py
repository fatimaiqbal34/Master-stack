import os

from dotenv import load_dotenv, find_dotenv
from groq import Groq


load_dotenv(find_dotenv())

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing. Please check your .env file.")

client = Groq(api_key=api_key)


SYSTEM_PROMPT = """
You are a friendly, helpful AI assistant on Fatima Iqbal's portfolio website.
Keep answers concise, clear, and conversational. You can discuss Fatima's
AI stack (Python, Machine Learning, Deep Learning, Generative AI, RAG, MCP,
AI Agents) if asked, but you can also chat about general topics.
"""


def chat_with_assistant(message: str, history: list):
    if not message or not message.strip():
        raise ValueError("Message cannot be empty.")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # history items come from the frontend as {role, content}
    for item in history or []:
        role = item.get("role") if isinstance(item, dict) else item.role
        content = item.get("content") if isinstance(item, dict) else item.content
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})

    # ensure the latest message is included
    if not messages or messages[-1].get("content") != message:
        messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        max_tokens=600,
        temperature=0.7,
    )

    return response.choices[0].message.content