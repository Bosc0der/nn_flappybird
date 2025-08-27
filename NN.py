import numpy as np
import matplotlib.pyplot as plt

# Simple one-layer neural network for vector input, with sigmoid hidden layer and sigmoid output (binary)
class NN:
    def __init__(self, n_neurons):
        n_inputs=4
        # W: (n_inputs, n_neurons)
        # Use uniform distribution instead of normal
        self.W = np.random.uniform(-10, 10, size=(n_inputs, n_neurons))
        self.b = np.random.uniform(-10, 10, size=(n_neurons,))
        self.W_out = np.random.uniform(-10, 10, size=(n_neurons,))
        self.b_out = np.random.uniform(-10,10)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
        
    def forward(self, X):
        # X: (n_samples, n_inputs) or (n_inputs,)
        X = np.atleast_2d(X)
        self.Z1 = X @ self.W + self.b  # (n_samples, n_neurons)
        self.A1 = self.sigmoid(self.Z1)
        self.Z2 = self.A1 @ self.W_out + self.b_out  # (n_samples,)
        self.A2 = self.sigmoid(self.Z2)  # Use sigmoid for binary output
        # Output a scalar 0 or 1
        return int(self.A2[0] >= 0.5)

   
