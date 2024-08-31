import mesa
import random

class TreeCell(mesa.Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        CHANGED : added probability to neighbouring trees : first layer, probability of burning is 85%
        trees around (neighbours around neighbours --> probability is 25%)
        """
        if self.condition == "On Fire":
            # Iterate through neighbors directly adjacent
            for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True, radius=1):
                if neighbor.condition == "Fine" and random.random() < 0.8:
                    neighbor.condition = "On Fire"

            # Iterate through neighbors of neighbors (second layer)
            for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True, radius=2):
                if neighbor.condition == "Fine" and random.random() < 0.05:
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"