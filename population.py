import numpy as np

from config import Y_LIM_TOP, Y_LIM_BOTOOM
from bird import Bird

class Population:
    def __init__(self, n_birds):
        self.n_birds = n_birds
        self.birds = [Bird() for _ in range(n_birds)]  # Store each bird's trajectory
    def how_many_alive(self):
        n_alive = sum(1 for bird in self.population.birds if bird.alive)
        print(n_alive)
    def update_all(self):
        for idx, bird in enumerate(self.birds):
            if bird.alive:
                bird.update()
        
    def restart(self):
        for bird in self.birds:
            bird.x=0
            bird.y = np.random.uniform(-10, 10)

    def mutate_all(self): 
        for bird in self.birds:
            bird.mutate()

    def next_generation_from_bird(self, parent_bird):
        """
        Replace the current population with mutated copies of the given parent bird.
        """
        self.birds = []
        for _ in range(self.n_birds):
            # Create a new bird and copy the parent's neural network weights
            new_bird = Bird()
            new_bird.nn.W = np.copy(parent_bird.nn.W)
            new_bird.nn.b = np.copy(parent_bird.nn.b)
            new_bird.nn.W_out = np.copy(parent_bird.nn.W_out)
            new_bird.nn.b_out = np.copy(parent_bird.nn.b_out)
            # Mutate the new bird
            new_bird.mutate()
            self.birds.append(new_bird)

        #
     
                

    

        
            

        
    
