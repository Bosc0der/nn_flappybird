import numpy as np

from config import Y_LIM_TOP, Y_LIM_BOTOOM
from bird import Bird

class Population:
    def __init__(self, n_birds):
        self.n_birds = n_birds
        self.birds = [Bird() for _ in range(n_birds)] 
        self.generation=0
         # Store each bird's trajectory

    def update_all(self):
        for bird in self.birds:
            if bird.alive:
                bird.update()

    def next_generation_from_bird(self, parent_bird):
        """
        Replace the current population with mutated copies of the given parent bird.
        """
        self.birds = [parent_bird]
        for _ in range(self.n_birds-1):
            # Create a new bird and copy the parent's neural network weights
            new_bird = Bird()
            # Set mutation parameters
            initial_mutation_rate = 3 
            decay=0.99999999
            mutation_rate=initial_mutation_rate * (decay ** self.generation)
           
            # Deep copy parent's neural network weights to ensure independent mutation
            new_bird.nn.W = np.copy(parent_bird.nn.W) + np.random.normal(loc=0, scale=mutation_rate, size=parent_bird.nn.W.shape)
            new_bird.nn.b = np.copy(parent_bird.nn.b) + np.random.normal(loc=0, scale=mutation_rate, size=parent_bird.nn.b.shape)
            new_bird.nn.W_out = np.copy(parent_bird.nn.W_out) + np.random.normal(loc=0, scale=mutation_rate, size=parent_bird.nn.W_out.shape)
            new_bird.nn.b_out = np.copy(parent_bird.nn.b_out) + np.random.normal(loc=0, scale=mutation_rate, size=())
            # Mutate the new bird's neural network
            #new_bird.mutate()
            self.birds.append(new_bird)


            
                # Call the find_ostacle method to update the bird's knowledge of the obstacle position
    

    

        
            

        
    
