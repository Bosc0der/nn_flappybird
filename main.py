from game import Game
import matplotlib.pyplot as plt

n_birds=1000
n_generations=100
game=Game(n_birds,n_generations)

for i in range(n_generations):
    game.run_generation()
    if i == 10:
        game.renderer.animate_generation()
    game.new_generation()
    
#




