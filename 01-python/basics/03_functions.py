# 03_functions.py

def greet(name):
    return f"Hello, {name}!"

print(greet("Claude"))


def build_config(model="claude-sonnet-5", temperature=0.7, max_tokens=1024):
    return {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

default_config = build_config()
custom_config = build_config(temperature=0.2, max_tokens=500)

print("Default config:", default_config)
print("Custom config:", custom_config)


def add_message(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

chat = [{"role": "user", "content": "Hi"}]
chat = add_message(chat, "assistant", "Hello there!")
chat = add_message(chat, "user", "Tell me a joke")

print("\nChat history:")
for msg in chat:
    print(f"  {msg['role']}: {msg['content']}")