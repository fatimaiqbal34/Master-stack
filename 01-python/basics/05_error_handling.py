# 05_error_handling.py

# Basic try/except — this pattern is used constantly in AI API calls
def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: cannot divide by zero"

print(divide(10, 2))
print(divide(10, 0))


# Real-world example: accessing a missing key in a dictionary
data = {"name": "Ali", "age": 20}

try:
    print(data["email"])
except KeyError:
    print("Error: 'email' key does not exist")


# Handling multiple exception types — API calls can fail for different reasons
def safe_api_call(should_fail_type=None):
    try:
        if should_fail_type == "network":
            raise ConnectionError("Network is down")
        elif should_fail_type == "value":
            raise ValueError("Invalid input provided")
        else:
            return "API call successful!"
    except ConnectionError as e:
        return f"Handled network error: {e}"
    except ValueError as e:
        return f"Handled value error: {e}"
    finally:
        print("(This always runs, whether an error happened or not)")

print(safe_api_call())
print(safe_api_call("network"))
print(safe_api_call("value"))