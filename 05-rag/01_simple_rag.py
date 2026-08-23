# 01_simple_rag.py
# A simple RAG system: answer questions using only provided documents

import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv(find_dotenv())
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Our "knowledge base" — normally this would be hundreds of documents
documents = [
    "The company's return policy allows returns within 30 days of purchase with a valid receipt.",
    "Our office hours are Monday to Friday, 9 AM to 6 PM. We are closed on public holidays.",
    "The premium subscription costs $15 per month and includes unlimited downloads.",
    "To reset your password, go to Settings > Account > Reset Password and follow the email link.",
    "Shipping usually takes 3-5 business days within the country, and 10-14 days internationally.",
]

# Step 1: Convert all documents into embeddings (do this once, upfront)
doc_embeddings = embedder.encode(documents)

def retrieve_relevant_doc(question, top_k=1):
    """Find the document(s) most similar in meaning to the question"""
    question_embedding = embedder.encode([question])
    similarities = cosine_similarity(question_embedding, doc_embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]
    return [documents[i] for i in top_indices]

def answer_question(question):
    # Step 2: Retrieve the most relevant document
    relevant_docs = retrieve_relevant_doc(question)
    context = "\n".join(relevant_docs)

    # Step 3: Ask Groq to answer using ONLY the retrieved context
    prompt = f"""Answer the question using ONLY the information in the context below. 
If the context doesn't contain the answer, say "I don't have that information."

Context:
{context}

Question: {question}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content, relevant_docs

print("=== Simple RAG System ===")
print("Ask a question. Type 'exit' to quit.\n")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break

    answer, sources = answer_question(question)
    print("\nAI:", answer)
    print("(Retrieved from:", sources[0][:60] + "...)\n")