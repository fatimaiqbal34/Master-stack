# 02_data_structures.py

# LIST — ordered collection, jaise conversation history
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"},
]

# DICT — key-value pairs, jaise API config ya request payload
config = {
    "model": "claude-sonnet-5",
    "temperature": 0.7,
    "max_tokens": 1024,
    "messages": messages,
}

print("First message role:", messages[0]["role"])
print("Model:", config["model"])

messages.append({"role": "user", "content": "What's the weather today?"})
print("Total messages now:", len(messages))

print("\nFull config:")
print(config)