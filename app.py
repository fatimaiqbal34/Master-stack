# app.py
# Main website combining all agents into one app

import os
import json
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from groq import Groq

load_dotenv(find_dotenv())

# Try environment variable first (for local development),
# fall back to Streamlit secrets (for cloud deployment)
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.set_page_config(page_title="My AI Agents", page_icon="🤖", layout="centered")

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("👋 About Me")
    st.write("Hi, I'm **Fatima Iqbal** — learning to build AI-powered applications from scratch.")
    st.write("This site showcases the AI agents I built while mastering the AI stack.")
    st.markdown("---")
    st.write("🔗 **Links**")
    st.write("[GitHub](https://github.com/fatimaiqbal34)")
    st.markdown("---")
    st.caption("Built with Python, Groq API & Streamlit")

# ---------- MAIN PAGE ----------
st.title("🤖 My AI Agents")
st.write("A collection of AI tools I built while learning the AI stack.")

tab1, tab2, tab3 = st.tabs(["📝 Blog Writer", "🧮 Reasoning Agent", "💬 Chat Assistant"])

# ---------- TAB 1: Blog Writer ----------
with tab1:
    st.header("Project-to-Blog Agent")
    st.write("Turn your rough project notes into a polished blog post.")

    BLOG_SYSTEM_PROMPT = """You are a professional technical writer who turns a developer's 
project notes into a polished, well-structured blog post suitable for a portfolio website.

CRITICAL RULE: Only mention tools, libraries, or challenges explicitly stated by the user. 
Never invent specifics. If detail is missing, keep that part general.

Output in Markdown: a title, then the post.
"""

    notes = st.text_area("Tell me about your project:", height=200, key="blog_notes")

    if st.button("Generate Blog Post", key="blog_btn"):
        if notes.strip() == "":
            st.warning("Please write something about your project first.")
        else:
            with st.spinner("Writing your blog post..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": BLOG_SYSTEM_PROMPT},
                        {"role": "user", "content": f"Notes:\n\n{notes}\n\nWrite the blog post."}
                    ],
                    max_tokens=1500,
                    temperature=0.7,
                )
                st.markdown("---")
                st.markdown(response.choices[0].message.content)

# ---------- TAB 2: Reasoning Agent ----------
with tab2:
    st.header("Reasoning Agent")
    st.write("Ask a question — this agent decides on its own whether it needs a tool.")

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

    question = st.text_input("Ask something:", key="reasoning_q")

    if st.button("Ask", key="reasoning_btn"):
        if question.strip() == "":
            st.warning("Type a question first.")
        else:
            with st.spinner("Thinking..."):
                messages = [{"role": "user", "content": question}]
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
                        st.info(f"🔧 Used tool: {fn_name}({fn_args})")
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
                    st.write(final.choices[0].message.content)
                else:
                    st.write(msg.content)

# ---------- TAB 3: Chat Assistant (with memory) ----------
with tab3:
    st.header("Chat Assistant")
    st.write("A simple conversational assistant with memory.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content": "You are a friendly, helpful assistant. Keep answers concise."}
        ]

    if st.button("Clear Chat", key="clear_chat_btn"):
        st.session_state.chat_history = [
            {"role": "system", "content": "You are a friendly, helpful assistant. Keep answers concise."}
        ]
        st.rerun()

    for msg in st.session_state.chat_history[1:]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_msg = st.chat_input("Type a message...")

    if user_msg:
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.write(user_msg)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=st.session_state.chat_history,
            max_tokens=500,
        )
        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

# ---------- FOOTER ----------
st.markdown("---")
st.caption("© 2026 Fatima Iqbal — Built while learning the AI stack.")