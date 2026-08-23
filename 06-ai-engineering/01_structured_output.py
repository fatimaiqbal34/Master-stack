# 01_structured_output.py
# Getting reliable, structured data from an LLM (not just free-form text)

import os
import json
from dotenv import load_dotenv, find_dotenv
from groq import Groq

load_dotenv(find_dotenv())
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Problem: normally AI gives free-form text, which is hard for code to use reliably.
# Solution: ask for JSON output with a clear schema, and parse it.

def extract_info(text):
    prompt = f"""Extract the following information from the text below and return ONLY valid JSON 
with no extra commentary, in this exact format:
{{
    "name": "string or null",
    "age": "number or null",
    "occupation": "string or null"
}}

Text: {text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        response_format={"type": "json_object"},  # forces valid JSON output
    )

    raw = response.choices[0].message.content
    return json.loads(raw)  # convert JSON text into a real Python dict


# Test it
sample_text = "Hi, I'm Ahmed, I'm 24 years old and I work as a software engineer."
result = extract_info(sample_text)

print("Extracted data (as a Python dict):")
print(result)
print("\nAccess individual fields:")
print("Name:", result["name"])
print("Age:", result["age"])
print("Occupation:", result["occupation"])