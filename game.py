import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from NN import NN
from bird import Bird
from population import Population
from obstacle import Obstacle
from config import T_ARRAY, Y_LIM_BOTOOM, Y_LIM_TOP, TIMESTEP
from renderer import Renderer

class Game:
    def __init__(self, n_birds, n_generations):
        self.n_birds = n_birds
        self.n_generations = n_generations
        self.obstacle = Obstacle(1, 1, 0.1, 5)
        self.population = Population(self.n_birds)
        self.max_distance=[]
        self.renderer=Renderer(self.population, self.obstacle, self.max_distance)


    def run_generation(self):
        # Simulate until all birds are dead
        while any(bird.alive for bird in self.population.birds):
            self.find_obstacle()
            self.population.update_all()
            self.collide_all()
            self.new_obstacle_if_passed()
    
    def new_obstacle_if_passed(self):
    # If any bird reaches or exceeds the obstacle's x set obstacle x_obs further and y_obs randomly
        if any(bird.x >= self.obstacle.x_obs+self.obstacle.x_width for bird in self.population.birds):
            self.obstacle.x_obs=self.obstacle.x_obs+1
            self.obstacle.y_obs=np.random.uniform(-7, 7)

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
        self.obstacle.x_obs=1
        self.population.next_generation_from_bird(best_bird)
        #generation counter
        self.population.generation=self.population.generation+1

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
