# 03_train_test_split.py
# Why we split data into training and testing sets

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import numpy as np

# More data this time (10 emails instead of 6)
X = np.array([
    [0, 0], [1, 0], [5, 1], [6, 1], [0, 1],
    [4, 1], [2, 0], [7, 1], [1, 1], [3, 0],
])
y = np.array([0, 0, 1, 1, 0, 1, 0, 1, 0, 0])

# Split: 70% for training, 30% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# Train ONLY on training data
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Check accuracy on data it HAS seen (training)
train_accuracy = model.score(X_train, y_train)

# Check accuracy on data it has NEVER seen (testing) — this is the real test
test_accuracy = model.score(X_test, y_test)

print("Accuracy on training data:", train_accuracy)
print("Accuracy on unseen test data:", test_accuracy)