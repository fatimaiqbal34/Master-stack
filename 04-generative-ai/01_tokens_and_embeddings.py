# 01_tokens_and_embeddings.py
# Understanding tokens — how LLMs actually "see" text

import tiktoken

# LLMs don't read words directly — they break text into "tokens" 
# (pieces of words, sometimes whole words, sometimes fragments)
encoder = tiktoken.get_encoding("cl100k_base")

text = "Machine learning is transforming how we build software."

tokens = encoder.encode(text)
print("Original text:", text)
print("Number of tokens:", len(tokens))
print("Token IDs:", tokens)

# Decode tokens back to see how the text was actually split
print("\nHow the text was split into pieces:")
for token in tokens:
    piece = encoder.decode([token])
    print(f"  {token} -> '{piece}'")

# This matters because:
# - APIs charge per token, not per word
# - max_tokens settings limit how much text can be generated
# - longer/unusual words often use MORE tokens than you'd expect