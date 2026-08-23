# 02_simple_eval.py
# A basic "eval" — testing if the AI gives correct answers consistently

import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq

load_dotenv(find_dotenv())
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define test cases: question + the expected correct answer (keyword to check for)
test_cases = [
    {"question": "What is 15 + 27?", "expected_keyword": "42"},
    {"question": "What is the capital of Japan?", "expected_keyword": "Tokyo"},
    {"question": "What is 2 to the power of 10?", "expected_keyword": "1024"},
]

def ask(question):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": question}],
        max_tokens=100,
    )
    return response.choices[0].message.content

def run_eval(test_cases):
    passed = 0
    for case in test_cases:
        answer = ask(case["question"])
        is_correct = case["expected_keyword"] in answer

        status = "✅ PASS" if is_correct else "❌ FAIL"
        print(f"{status} | Q: {case['question']}")
        print(f"   Expected keyword: '{case['expected_keyword']}' | Got: {answer[:80]}")

        if is_correct:
            passed += 1

    print(f"\nScore: {passed}/{len(test_cases)}")

run_eval(test_cases)