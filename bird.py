import numpy as np
import matplotlib.pyplot as plt
from NN import NN
from obstacle import Obstacle
from config import G,TIMESTEP, V_REBOUND, Y_LIM_BOTOOM, Y_LIM_TOP

class Bird:
    def __init__(self):
        # Import external variables from global scope
        global TIMESTEP, G, V_REBOUND
        self.g = G
        self.vx = 1
        self.timestep = TIMESTEP
        # Set initial conditions randomly
        self.x = 0
        self.y = np.random.uniform(-10, 10)
        self.vy = 0
        self.r = [self.x, self.y, self.vy]
        self.nn = NN(100)
        self.alive = True
        self.yobs=0
        self.xobs=0
        self.trajectory=[]

    def control_u_NN(self):
        X = np.array([[self.x, self.y, self.vy, self.xobs, self.yobs]])
        u = self.nn.forward(X)
        return u

    def dynamics(self):
        u = self.control_u_NN()
        drdt = [
            self.vx,
            self.vy,
            self.g + u * (-self.g - self.vy / self.timestep + V_REBOUND)
        ]
        return drdt

    def update(self):
        drdt = self.dynamics()
        self.x = self.x + drdt[0] * self.timestep
        self.y = self.y + drdt[1] * self.timestep
        self.vy = self.vy + drdt[2] * self.timestep
        self.r = [self.x, self.y, self.vy]


    def mutate(self):
        # Use the mean of the current bird's weights as the mean for mutation
        mean_W = np.mean(self.nn.W)
        mean_b = np.mean(self.nn.b)
        mean_W_out = np.mean(self.nn.W_out)
        mean_b_out = np.mean(self.nn.b_out)
        self.nn.W = np.random.normal(loc=mean_W, scale=0.001, size=self.nn.W.shape)
        self.nn.b = np.random.normal(loc=mean_b, scale=0.001, size=self.nn.b.shape)
        self.nn.W_out = np.random.normal(loc=mean_W_out, scale=0.001, size=self.nn.W_out.shape)
        self.nn.b_out = np.random.normal(loc=mean_b_out, scale=0.001, size=())

