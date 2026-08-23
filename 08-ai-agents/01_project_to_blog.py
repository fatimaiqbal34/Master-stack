# 01_project_to_blog.py
import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq

load_dotenv(find_dotenv())
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a professional technical writer who turns a developer's project notes 
into a polished, well-structured blog post suitable for a portfolio website or LinkedIn article.

Guidelines:
- Professional, clear, and confident tone — no slang, no filler phrases
- Structure: a strong title, a brief introduction (what the project is and why it was built),
  a section on the technical approach/implementation, a section on challenges faced and how 
  they were solved, and a closing section on key takeaways or skills demonstrated

CRITICAL RULE — DO NOT INVENT DETAILS:
- Only mention tools, libraries, techniques, or challenges that the person explicitly stated
- If the person did not mention a specific library, tool, database, or technique, 
  do NOT name one — describe that part generically instead 
  (e.g., "processed and validated the input data" instead of naming a specific library)
- If the person did not describe a challenge they faced, do NOT invent one
- If a section would require invented specifics to sound complete, keep that section 
  brief and general rather than filling it with fabricated detail
- It is better to write a shorter, accurate post than a longer post with invented facts

- Use precise, industry-appropriate language (e.g., "implemented", "resolved", "integrated")
- Avoid generic buzzwords like "game-changer", "revolutionize", "unlock the power of"
- Keep paragraphs concise and scannable, use subheadings

Output in Markdown: a title, then the post. Nothing else — no meta-commentary before or after.
"""

print("=== Project-to-Blog Agent ===")
print("Tell me about your project (what you built, what problems you hit, what you learned).")
print("The more detail you give, the better the post. Type 'DONE' on a new line when finished.\n")

lines = []
while True:
    line = input()
    if line.strip().upper() == "DONE":
        break
    lines.append(line)

notes = "\n".join(lines)

print("\nWriting the blog post...\n")

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Here are my rough notes about a project:\n\n{notes}\n\nWrite the blog post."}
    ],
    max_tokens=1500,
    temperature=0.9,
)

post = response.choices[0].message.content
print(post)

with open("blog_post.md", "w", encoding="utf-8") as f:
    f.write(post)

print("\nSaved to 'blog_post.md'.")