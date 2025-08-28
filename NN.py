import numpy as np
import matplotlib.pyplot as plt

# Simple one-layer neural network for vector input, with sigmoid hidden layer and sigmoid output (binary)
class NN:
    def __init__(self, n_neurons):
        n_inputs=4
        # W: (n_inputs, n_neurons)
        # Use uniform distribution instead of normal
        # Xavier initialization for weights
        limit_W = np.sqrt(6 / (n_inputs + n_neurons))
        self.W = np.random.uniform(-limit_W, limit_W, size=(n_inputs, n_neurons))
        self.b = np.zeros((n_neurons,))
        limit_W_out = np.sqrt(6 / (n_neurons + 1))
        self.W_out = np.random.uniform(-limit_W_out, limit_W_out, size=(n_neurons,))
        self.b_out = 0.0

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

   
