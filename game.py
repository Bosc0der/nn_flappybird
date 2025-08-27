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
        self.obstacle = Obstacle(3, 1, 0.1, 3)
        self.population = Population(self.n_birds)
    

    def run_generation(self):
        
        # Simulate until all birds are dead
        while any(bird.alive for bird in self.population.birds):
            plt.close()
            self.plot_trajectories_and_obstacle()
   
            self.population.pop_find_obstacle(self.obstacle.y_obs,self.obstacle.x_obs)
            self.population.update_all()
            self.collide_all()
    # If any bird reaches or exceeds the obstacle's x position, reset all birds' x to 0 and set obstacle y_obs randomly
            if any(bird.x >= self.obstacle.x_obs+self.obstacle.x_width for bird in self.population.birds):
                # Reset all birds' x to 0
                print('pass')
                for bird in self.population.birds:
                    bird.x = 0
                    self.obstacle.y_obs=np.random.uniform(-7, 7)
                    self.population.pop_find_obstacle(self.obstacle.y_obs,self.obstacle.x_obs)
                
                # Set obstacle y_obs to a new random value within allowed bounds
                #self.obstacle.y_obs = np.random.uniform(Y_LIM_BOTOOM, Y_LIM_TOP - self.obstacle.y_width)
            

    def new_generation(self):
        # Find the last living bird (the one that survived the longest)
        last_living_bird = max(self.population.birds, key=lambda b: len(b.trajectory))
        self.population.next_generation_from_bird(last_living_bird)
       
        

    def plot_trajectories_and_obstacle(self):
        """
        Plot the trajectories of all birds in the current population and the obstacle.
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        # Use the draw method from Population to plot all birds' trajectories
        self.population.draw(ax)
        # Draw the obstacle
        self.obstacle.draw(ax)
        ax.set_xlim(0, 5)
        ax.set_ylim(Y_LIM_BOTOOM, Y_LIM_TOP)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Birds' Trajectories and Obstacle")
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
