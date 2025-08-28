from game import Game
import matplotlib.pyplot as plt

n_birds=100
n_generations=1000
game=Game(n_birds,n_generations)
game.generation_to_plot=50

for i in range(n_generations):
    game.run_generation()
    print('generation'+str(i))
    
    # if i %10==0:
    #     game.plot_max_distance() 
        
    # #     game.plot_trajectories_and_obstacle()
    #     
    game.new_generation()
    
 

 
    

#




