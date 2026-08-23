# 01_intro_ml.py
# Machine Learning basics: teaching a computer to find patterns in data

from sklearn.linear_model import LinearRegression
import numpy as np

# Example: predicting house price based on size (sq ft)
# X = input data (features), y = what we want to predict (target)
X = np.array([[500], [750], [1000], [1250], [1500]])  # house sizes
y = np.array([50000, 75000, 100000, 125000, 150000])   # house prices

# Create and train the model
model = LinearRegression()
model.fit(X, y)

# Predict the price of a new house
new_house_size = np.array([[1100]])
predicted_price = model.predict(new_house_size)

print("Predicted price for a 1100 sq ft house:", predicted_price[0])

# What the model learned
print("Slope (price per sq ft):", model.coef_[0])
print("Base price:", model.intercept_)