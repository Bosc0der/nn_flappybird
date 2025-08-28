import matplotlib.pyplot as plt
import numpy as np
from config import Y_LIM_BOTOOM, Y_LIM_TOP

from matplotlib import animation

class Renderer:
    def __init__(self, population, obstacle, max_distance, ax=None):
        self.population = population
        self.obstacle = obstacle
        self.max_distance = max_distance
        self.ax = ax

    def draw_bird(self, ax):
        for bird in self.population.birds:
            traj = np.array(bird.trajectory)
            if len(traj) > 1:
                ax.plot(traj[:, 0], traj[:, 1], alpha=0.7)

    def draw_obstacle(self, ax, color='red', **kwargs):
        import matplotlib.patches as patches
        rect = patches.Rectangle(
            (self.obstacle.x_obs, self.obstacle.y_obs),
            self.obstacle.x_width,
            self.obstacle.y_width,
            linewidth=1,
            edgecolor=color,
            facecolor=color,
            **kwargs
        )
        ax.add_patch(rect)
        return rect

    def plot_max_distance(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(self.max_distance)
        ax.set_xlabel("Generation")
        ax.set_ylabel("Max Distance")
        ax.set_title("Max Distance per Generation")
        plt.tight_layout()

    def animate_generation(self, interval=50, save_path=None):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_xlim(0, max([bird.x for bird in self.population.birds] + [self.obstacle.x_obs + self.obstacle.x_width, 10]))
        ax.set_ylim(Y_LIM_BOTOOM, Y_LIM_TOP)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"Generation {self.population.generation}")
        plt.tight_layout()

        lines = [ax.plot([], [], lw=2, alpha=0.7)[0] for _ in self.population.birds]
        rect = self.draw_obstacle(ax, alpha=0.5)

        max_len = max(len(bird.trajectory) for bird in self.population.birds)

        def get_traj(bird, i):
            traj = np.array(bird.trajectory)
            if len(traj) > i:
                return traj[:i+1, 0], traj[:i+1, 1]
            return traj[:, 0], traj[:, 1]

        def init():
            for line in lines:
                line.set_data([], [])
            return lines + [rect]

        def animate(i):
            for idx, bird in enumerate(self.population.birds):
                x, y = get_traj(bird, i)
                lines[idx].set_data(x, y)
            return lines + [rect]

        ani = animation.FuncAnimation(
            fig, animate, init_func=init, frames=max_len, interval=interval, blit=True
        )

        if save_path:
            ani.save(save_path, writer='ffmpeg')
        else:
            plt.show()
        return ani

