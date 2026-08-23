# 02_reasoning_agent.py
# An agent that decides which tool to use based on the user's question

import os
import json
from dotenv import load_dotenv, find_dotenv
from groq import Groq

load_dotenv(find_dotenv())
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- Tools the agent can use ---

def calculate(expression):
    try:
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return f"Error: {e}"

def word_count(text):
    return str(len(text.split()))

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluates a math expression",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "word_count",
            "description": "Counts words in a piece of text",
            "parameters": {
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
        },
    },
]

available_functions = {"calculate": calculate, "word_count": word_count}

def run_agent(user_message):
    messages = [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=tools,
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)
        for call in msg.tool_calls:
            fn_name = call.function.name
            fn_args = json.loads(call.function.arguments)
            print(f"  [Agent decided to use: {fn_name}({fn_args})]")

            result = available_functions[fn_name](**fn_args)
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result,
            })

        final = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
        )
        return final.choices[0].message.content
    else:
        return msg.content


print("=== Reasoning Agent ===")
print("Ask anything. Type 'exit' to quit.\n")

while True:
    q = input("You: ")
    if q.lower() == "exit":
        break
    answer = run_agent(q)
    print("AI:", answer, "\n")