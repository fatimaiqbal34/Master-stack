import os

from dotenv import load_dotenv, find_dotenv
from groq import Groq


load_dotenv(find_dotenv())

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing. Please check your .env file.")

client = Groq(api_key=api_key)


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


def generate_blog(notes: str) -> str:
    """Takes raw project notes and returns a polished Markdown blog post."""

    if not notes or not notes.strip():
        raise ValueError("Project notes cannot be empty.")

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Here are my rough notes about a project:\n\n"
                    f"{notes}\n\n"
                    "Write the blog post."
                ),
            },
        ],
        max_tokens=1500,
        temperature=0.9,
    )

    return response.choices[0].message.content


# --- Only runs when this file is executed directly (e.g. `python blog_agent.py`) ---
# It will NOT run when FastAPI imports this file, so the server won't hang waiting for input.
if __name__ == "__main__":
    print("=== Project-to-Blog Agent (standalone terminal mode) ===")
    print("Tell me about your project. Type 'DONE' on a new line when finished.\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)

    user_notes = "\n".join(lines)
    print("\nWriting the blog post...\n")

    blog_post = generate_blog(user_notes)
    print(blog_post)

    with open("blog_post.md", "w", encoding="utf-8") as f:
        f.write(blog_post)

    print("\nSaved to 'blog_post.md'.")