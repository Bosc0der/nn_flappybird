from game import Game
import matplotlib.pyplot as plt
n_birds=100
n_generations=1000
game=Game(n_birds,n_generations)

for i in range(n_generations):
    game.run_generation()
    # plt.close()
    # if i %10==0:
        
    # #     game.plot_trajectories_and_obstacle()
    #     game.plot_max_distance() 
    game.new_generation()
    
 

 
    

#




