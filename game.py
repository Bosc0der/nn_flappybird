import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from NN import NN
from bird import Bird
from population import Population
from obstacle import Obstacle
from config import T_ARRAY, Y_LIM_BOTOOM, Y_LIM_TOP, TIMESTEP

class Game:
    def __init__(self, n_birds, n_generations):
        self.n_birds = n_birds
        self.n_generations = n_generations
        self.obstacle = Obstacle(3, 1, 1, 2)#if obstacle is too thin and timestep to large, bird might teleport to the other side
        self.population = Population(self.n_birds)
        self.max_distance=[]
        self.generations_to_plot = set(range(20, 51))  # Plot generations 20 to 50 inclusive
        # --- For persistent plotting to avoid flicker ---
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self._plot_initialized = False
        

    def run_generation(self):
        self.find_obstacle()
        # Simulate until all birds are dead
        while any(bird.alive for bird in self.population.birds):
            # Plot only for specified generations
            if self.population.generation in self.generations_to_plot:
                self.plot_trajectories_and_obstacle()
            self.population.update_all()
            self.collide_all()
            self.update_obstacle_if_passed()
        # No plt.close() here to avoid flicker

    def update_obstacle_if_passed(self):
        if any(bird.x >= self.obstacle.x_obs+self.obstacle.x_width for bird in self.population.birds):
            self.obstacle.x_obs=self.obstacle.x_obs+3
            self.obstacle.y_obs=np.random.uniform(-7, 7)
            self.find_obstacle()

    def find_obstacle(self):   
         for bird in self.population.birds:
                bird.xobs_bird=abs(self.obstacle.x_obs-bird.x)
                bird.yobs_bird=self.obstacle.y_obs   
            
    def new_generation(self):
        # All birds are dead, so select the bird that survived the longest (i.e., has the longest trajectory)
        # Find the bird with the longest trajectory (i.e., survived the longest)
        best_bird = max(self.population.birds, key=lambda bird: bird.x)
        print(best_bird.x)
        self.max_distance.append(best_bird.x)
        self.obstacle.y_obs=np.random.uniform(-7, 7)
        self.population.next_generation_from_bird(best_bird)
        self.obstacle.x_obs=3
        #generation counter
        self.population.generation=self.population.generation+1

    def plot_trajectories_and_obstacle(self):
        # Plot only for specified generations
        if self.population.generation not in self.generations_to_plot:
            return
        # Use persistent figure/axes to avoid flicker
        ax = self.ax
        ax.clear()
        self.population.draw(ax)
        
        # --- Draw all past obstacles as faded rectangles ---
        if not hasattr(self, 'obstacle_history'):
            self.obstacle_history = []
        # Add current obstacle to history if new
        if (not self.obstacle_history) or (
            self.obstacle_history[-1][0] != self.obstacle.x_obs or
            self.obstacle_history[-1][1] != self.obstacle.y_obs
        ):
            self.obstacle_history.append((
                self.obstacle.x_obs, self.obstacle.y_obs, self.obstacle.x_width, self.obstacle.y_width
            ))
        # Draw all obstacles in history, faded except the last (current)
        for i, (x_obs, y_obs, x_width, y_width) in enumerate(self.obstacle_history):
            color = 'red'
            alpha = 0.2 if i < len(self.obstacle_history) - 1 else 1.0
            # Draw using Obstacle's draw method
            obs = Obstacle(x_obs, y_obs, x_width, y_width)
            obs.draw(ax, color=color, alpha=alpha)
        
        ax.set_ylim(Y_LIM_BOTOOM, Y_LIM_TOP)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        # Dynamically center x-limits on the best (farthest) bird
        if self.population.birds:
            # Find the bird with the maximum x (farthest right)
            max_x = max(bird.x for bird in self.population.birds)
            # Center the view around the farthest bird, with a window of width 10
            x_window = 2.9
            ax.set_xlim(max_x - x_window/4, max_x + x_window/2)
        ax.set_title(f"Generation {self.population.generation}")
        plt.tight_layout()
        plt.pause(0.01) 
        
    def plot_max_distance(self):
        # Use a separate persistent figure for max distance plot
        if not hasattr(self, 'fig_max'):
            self.fig_max, self.ax_max = plt.subplots(figsize=(8, 6))
        ax = self.ax_max
        ax.clear()
        ax.plot(self.max_distance)
        ax.set_xlabel("Generation")
        ax.set_ylabel("Max Distance")
        ax.set_title("Max Distance per Generation")
        plt.tight_layout()
        plt.pause(0.01) 
        
    def collide_all(self):
        for bird in self.population.birds:
            if bird.alive:
                x_obs = self.obstacle.x_obs
                y_obs = self.obstacle.y_obs
                x_width = self.obstacle.x_width
                y_width = self.obstacle.y_width

                # Fix collision logic: y_obs <= bird.y <= y_obs + y_width
                if (x_obs <= bird.x <= x_obs + x_width) and not (y_obs <= bird.y <= y_obs + y_width):
                    bird.alive = False
                # Collision with game boundaries (example: y out of bounds)
                if bird.y < Y_LIM_BOTOOM or bird.y > Y_LIM_TOP:
                    bird.alive = False
                    bird.alive = False
