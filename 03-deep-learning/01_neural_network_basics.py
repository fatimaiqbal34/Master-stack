# 01_neural_network_basics.py
# A tiny neural network from scratch — understanding the core building block

import torch
import torch.nn as nn

# A neural network is made of "neurons" that take inputs, multiply by weights, 
# add a bias, and pass through an activation function.

# Let's build the simplest possible network:
# Input: 2 numbers -> Output: 1 number

class SimpleNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer = nn.Linear(2, 1)  # 2 inputs, 1 output

    def forward(self, x):
        return self.layer(x)

model = SimpleNetwork()

# Try feeding it some input
sample_input = torch.tensor([[3.0, 5.0]])
output = model(sample_input)

print("Input:", sample_input)
print("Output (untrained, random weights):", output)

# See what weights and bias the network currently has (randomly initialized)
print("\nWeights:", model.layer.weight)
print("Bias:", model.layer.bias)