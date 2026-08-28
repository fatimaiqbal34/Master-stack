import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def chat_with_assistant(message: str, history=None):
    if history is None:
        history = []

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

    for item in history:
        if hasattr(item, "role") and hasattr(item, "content"):
            messages.append({"role": item.role, "content": item.content})
        elif isinstance(item, dict):
            messages.append(
                {
                    "role": item.get("role", "user"),
                    "content": item.get("content", ""),
                }
            )

    messages.append({"role": "user", "content": message})

    try:
        # Using available active Groq model
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
        )
        return completion.choices[0].message.content

    except Exception as e:
        print(f"Error in Groq Chat Agent: {str(e)}")
        raise Exception(f"Chat Agent Error: {str(e)}")