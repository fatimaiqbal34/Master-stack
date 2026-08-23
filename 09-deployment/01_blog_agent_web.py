# 01_blog_agent_web.py
import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from groq import Groq

load_dotenv(find_dotenv())
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a professional technical writer who turns a developer's project notes 
into a polished, well-structured blog post suitable for a portfolio website or LinkedIn article.

CRITICAL RULE: Only mention tools, libraries, or challenges explicitly stated by the user. 
Never invent specifics. If detail is missing, keep that part general.

Output in Markdown: a title, then the post.
"""

st.title("📝 Project-to-Blog Agent")
st.write("Turn your rough project notes into a polished blog post.")

notes = st.text_area("Tell me about your project:", height=200)

if st.button("Generate Blog Post"):
    if notes.strip() == "":
        st.warning("Please write something about your project first.")
    else:
        with st.spinner("Writing your blog post..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Notes:\n\n{notes}\n\nWrite the blog post."}
                ],
                max_tokens=1500,
                temperature=0.7,
            )
            post = response.choices[0].message.content
            st.markdown("---")
            st.markdown(post)