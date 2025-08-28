class Obstacle:
    def __init__(self, x_obs, y_obs, x_width, y_width):
        self.x_obs = x_obs
        self.y_obs = y_obs
        # Add x_width and y_width; if not provided, default to width
        self.x_width = x_width 
        self.y_width = y_width 
    
    