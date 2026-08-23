# 02_chat_loop.py
import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq

load_dotenv(find_dotenv())
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# This list holds the full conversation history
conversation = [
    {"role": "system", "content": "You are a friendly assistant helping a beginner learn to code. Keep answers short and simple."}
]

print("Chat started — type 'exit' to quit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bye!")
        break

    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        max_tokens=300,
        messages=conversation,
    )

    reply = response.choices[0].message.content
    print("AI:", reply, "\n")

    conversation.append({"role": "assistant", "content": reply})