from game import Game
import matplotlib.pyplot as plt
n_birds=100
n_generations=1000
game=Game(n_birds,n_generations)

for i in range(n_generations):
    
    game.run_generation()
    game.plot_trajectories_and_obstacle()
    game.new_generation()
    #game.plot_max_distance()
    plt.close()
    
    

#




