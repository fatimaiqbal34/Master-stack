import os
import ast
import operator

from dotenv import load_dotenv, find_dotenv
from groq import Groq


load_dotenv(find_dotenv())

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing. Please check your .env file.")

client = Groq(api_key=api_key)


SYSTEM_PROMPT = """
You are a reasoning assistant. You have access to two tools:

- calculator: use this for any arithmetic / math question.
- word_counter: use this when asked to count words in a piece of text.

Only use a tool when the question actually needs it. For general knowledge
or conversational questions, answer directly without calling a tool.

Give clear, concise final answers.
"""


# ---------- Safe calculator (no eval/exec — restricted AST evaluation) ----------

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed.")

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_safe_eval(node.operand))

    raise ValueError("Unsupported or unsafe expression.")


def calculator(expression: str):
    tree = ast.parse(expression, mode="eval")
    result = _safe_eval(tree.body)
    return result


def word_counter(text: str):
    return len(text.split())


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a basic arithmetic expression and return the numeric result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A math expression, e.g. '456 * 78'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "word_counter",
            "description": "Count the number of words in a given piece of text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to count words in",
                    }
                },
                "required": ["text"],
            },
        },
    },
]

AVAILABLE_FUNCTIONS = {
    "calculator": calculator,
    "word_counter": word_counter,
}


def ask_reasoning_agent(question: str):
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        max_tokens=800,
        temperature=0.3,
    )

    message = response.choices[0].message
    tool_calls = message.tool_calls
    tool_used = None

    if tool_calls:
        messages.append(message)

        for call in tool_calls:
            fn_name = call.function.name

            import json
            fn_args = json.loads(call.function.arguments)

            fn = AVAILABLE_FUNCTIONS.get(fn_name)
            result = fn(**fn_args) if fn else "Tool not found."
            tool_used = fn_name

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": fn_name,
                    "content": str(result),
                }
            )

        follow_up = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            max_tokens=500,
            temperature=0.3,
        )

        final_answer = follow_up.choices[0].message.content
    else:
        final_answer = message.content

    return {
        "answer": final_answer,
        "tool_used": tool_used,
    }