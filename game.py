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
        self.obstacle = Obstacle(1.5, 1, 0.1, 3)
        self.population = Population(self.n_birds)
        # Store trajectories for all generations
        self.all_generations_trajectories = []  # List of list of bird trajectories per generation

    def run(self):
        for i in range(self.n_generations):
            T = 0
            # Reset trajectories for this generation
            for bird in self.population.birds:
                bird.yobs = self.obstacle.y_obs
                bird.xobs = self.obstacle.x_obs
                bird.trajectory = [[bird.x, bird.y]]  # Start trajectory

            # Store trajectories for this generation
            generation_trajectories = [[] for _ in range(self.n_birds)]

            while any(bird.alive for bird in self.population.birds):
                self.population.update_all()
                self.collide_all()
                # Append current position to each bird's trajectory
                for idx, bird in enumerate(self.population.birds):
                    if bird.alive:
                        bird.trajectory.append([bird.x, bird.y])
                T += TIMESTEP

            # After the generation, store all bird trajectories
            for idx, bird in enumerate(self.population.birds):
                # Copy the trajectory to avoid mutation in next generation
                generation_trajectories[idx] = np.array(bird.trajectory)
            self.all_generations_trajectories.append(generation_trajectories)

            # Find the last living bird (the one that survived the longest)
            last_living_bird = max(self.population.birds, key=lambda b: len(b.trajectory))
            self.population.next_generation_from_bird(last_living_bird)
            self.population.restart()
            print('generation' + str(i))

    def show(self):
        # Show trajectories of each generation
        n_gen = len(self.all_generations_trajectories)
        fig, axes = plt.subplots(1, n_gen, figsize=(6 * n_gen, 5), squeeze=False)
        for i, generation_trajectories in enumerate(self.all_generations_trajectories):
            ax = axes[0, i]
            for traj in generation_trajectories:
                traj = np.array(traj)
                if len(traj) > 1:
                    ax.plot(traj[:, 0], traj[:, 1], alpha=0.5)
            # Draw obstacle
            self.obstacle.draw(ax)
            ax.set_title(f"Generation {i}")
            ax.set_xlim(0,5)
            ax.set_ylim(Y_LIM_BOTOOM, Y_LIM_TOP)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
        plt.tight_layout()
        plt.show()

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

        #
