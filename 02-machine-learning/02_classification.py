# 02_classification.py
# Classification: predicting a category instead of a number

from sklearn.tree import DecisionTreeClassifier
import numpy as np

# Example: predicting if an email is spam based on 2 features:
# [number of exclamation marks, contains word "free" (1=yes, 0=no)]
X = np.array([
    [0, 0],   # normal email
    [1, 0],   # normal email
    [5, 1],   # spam
    [6, 1],   # spam
    [0, 1],   # normal-ish
    [4, 1],   # spam
])
y = np.array([0, 0, 1, 1, 0, 1])  # 0 = not spam, 1 = spam

model = DecisionTreeClassifier()
model.fit(X, y)

# Predict a new email: 3 exclamation marks, contains "free"
new_email = np.array([[3, 1]])
prediction = model.predict(new_email)

print("Prediction (0=not spam, 1=spam):", prediction[0])

# Check accuracy on training data
accuracy = model.score(X, y)
print("Accuracy on training data:", accuracy)