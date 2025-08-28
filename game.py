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
        self.obstacle = Obstacle(1, 1, 0.1, 5)
        self.population = Population(self.n_birds)
        self.max_distance=[]
    
    def run_generation(self):
        # Simulate until all birds are dead
        while any(bird.alive for bird in self.population.birds):
            plt.close()
            #self.plot_trajectories_and_obstacle()
            self.find_obstacle()
            self.population.update_all()
            self.collide_all()
            
    # If any bird reaches or exceeds the obstacle's x set obstacle x_obs further and y_obs randomly
            if any(bird.x >= self.obstacle.x_obs+self.obstacle.x_width for bird in self.population.birds):
                self.obstacle.x_obs=2*self.obstacle.x_obs
                self.obstacle.y_obs=np.random.uniform(-7, 7)
                self.find_obstacle()

    def find_obstacle(self):   
         for bird in self.population.birds:
                bird.xobs=abs(self.obstacle.x_obs-bird.x)
                bird.yobs=self.obstacle.y_obs    
            
    def new_generation(self):
        # All birds are dead, so select the bird that survived the longest (i.e., has the longest trajectory)
        # Find the bird with the longest trajectory (i.e., survived the longest)
        best_bird = max(self.population.birds, key=lambda bird: bird.x)
        print(best_bird.x)
        self.max_distance.append(best_bird.x)
        self.obstacle.y_obs=np.random.uniform(-7, 7)
        self.obstacle.x_obs=1
        self.population.next_generation_from_bird(best_bird)
        #generation counter
        self.population.generation=self.population.generation+1

    def plot_trajectories_and_obstacle(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        self.population.draw(ax)
        self.obstacle.draw(ax)
        ax.set_ylim(Y_LIM_BOTOOM, Y_LIM_TOP)
        ax.set_xlim(0,2)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"Generation {self.population.generation}")
        plt.tight_layout()
        
        plt.pause(0.01) 
        
    def plot_max_distance(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(self.max_distance)
        ax.set_xlabel("Generation")
        ax.set_ylabel("Max Distance")
        ax.set_title("Max Distance per Generation")
        plt.tight_layout()
        
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
