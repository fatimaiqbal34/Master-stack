# 02_training_a_network.py
# Training a neural network to learn a simple pattern: y = 2x + 1

import torch
import torch.nn as nn

# Training data: input x, and correct output y (following y = 2x + 1)
X = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0]])
y = torch.tensor([[3.0], [5.0], [7.0], [9.0], [11.0]])

# A simple 1-input, 1-output network
model = nn.Linear(1, 1)

# Loss function: measures how wrong the predictions are
loss_fn = nn.MSELoss()

# Optimizer: adjusts the weights to reduce the loss over time
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# Training loop — this is where "learning" actually happens
for epoch in range(200):
    predictions = model(X)
    loss = loss_fn(predictions, y)

    optimizer.zero_grad()
    loss.backward()      # calculate how to adjust weights
    optimizer.step()     # actually adjust the weights

    if epoch % 40 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

# Test the trained model
test_input = torch.tensor([[10.0]])
prediction = model(test_input)
print("\nPrediction for x=10 (expected ~21):", prediction.item())

print("Learned weight (expected ~2):", model.weight.item())
print("Learned bias (expected ~1):", model.bias.item())