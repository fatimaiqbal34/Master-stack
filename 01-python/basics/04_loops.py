# 04_loops.py

# FOR loop
messages = ["Hi", "How are you?", "Bye"]

for msg in messages:
    print("Message:", msg)

# WHILE loop
count = 0
while count < 3:
    print("Count is:", count)
    count += 1

# Loop se list banana — AI code mein bohot common pattern
roles = ["user", "assistant", "user"]
formatted = []

for r in roles:
    formatted.append({"role": r, "content": "sample text"})

print("\nFormatted messages:")
for item in formatted:
    print(item)