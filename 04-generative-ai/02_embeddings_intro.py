# 02_embeddings_intro.py
# Embeddings: turning text into numbers that capture MEANING

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# This model converts text into a list of numbers (a "vector") 
# that represents the text's meaning
model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "I love programming in Python",
    "Python is my favorite coding language",
    "The weather is sunny today",
]

embeddings = model.encode(sentences)

print("Shape of embeddings:", embeddings.shape)  # (3 sentences, N numbers each)
print("\nFirst 10 numbers of sentence 1's embedding:")
print(embeddings[0][:10])

# Now let's measure how SIMILAR the meanings are
similarity_1_2 = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
similarity_1_3 = cosine_similarity([embeddings[0]], [embeddings[2]])[0][0]

print(f"\nSimilarity between sentence 1 & 2 (both about Python): {similarity_1_2:.4f}")
print(f"Similarity between sentence 1 & 3 (Python vs weather): {similarity_1_3:.4f}")