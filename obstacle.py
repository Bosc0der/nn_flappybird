class Obstacle:
    def __init__(self, x_obs, y_obs, x_width, y_width):
        self.x_obs = x_obs
        self.y_obs = y_obs
        # Add x_width and y_width; if not provided, default to width
        self.x_width = x_width 
        self.y_width = y_width 
    
    # INSERT_YOUR_CODE
    def draw(self, ax, color='red', **kwargs):
        """
        Draw the obstacle as a colored square on the given matplotlib axis.
        """
        rect = None
        
        import matplotlib.patches as patches
        rect = patches.Rectangle(
            (self.x_obs, self.y_obs), 
            self.x_width, 
            self.y_width, 
            linewidth=1, 
            edgecolor=color, 
            facecolor=color, 
            **kwargs
        )
        ax.add_patch(rect)
    # If matplotlib is not available, do nothing
        return rect