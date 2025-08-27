# config.py
import numpy as np
# Define time parameters outside the class
T_START = 0
T_END = 3
N_POINTS = 250
TIMESTEP = (T_END - T_START) / N_POINTS
T_ARRAY = np.linspace(T_START, T_END, N_POINTS)
V_REBOUND=500
G = -9.8*5  # Gravity constant, adjust as needed

Y_LIM_BOTOOM=-10
Y_LIM_TOP=10
# Add other global constants here as needed
