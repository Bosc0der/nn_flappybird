from game import Game
n_birds=100
n_generations=3
game=Game(n_birds,n_generations)

for i in range(n_generations):
    game.run_generation()
    game.plot_trajectories_and_obstacle()
    game.new_generation()
    print('generation' + str(i))






