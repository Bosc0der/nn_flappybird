from game import Game
import matplotlib.pyplot as plt
from obstacle import Obstacle

n_birds=100
n_generations=1000
game=Game(n_birds,n_generations)
game.obstacle = Obstacle(3, 1, 0.1, 2) #x_obs, y_obs, x_width, y_width

#if obstacle is too thin and timestep to large, bird might teleport to the other side x_width > dx=vx*dt 

game.generations_to_plot= set(range(90,91)) 

for i in range(n_generations):
    game.run_generation()
    print('generation'+str(i))
    print(game.population.mutation_rate)
    
    # if i %10==0:
    #     game.plot_max_distance() 
        
    # #     game.plot_trajectories_and_obstacle()
    #     
    game.new_generation()
    
 

 
    

#




