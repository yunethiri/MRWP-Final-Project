import warnings
warnings.filterwarnings('ignore')

import mesa
from .agent import TreeCell


class ForestFire(mesa.Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, spatial_pattern = "Random"):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.

        """
        super().__init__()
        self.height = height
        self.width = width
        self.density = density
        self.spatial_pattern = spatial_pattern
        # Set up model objects
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=False)

        self.datacollector = mesa.DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "Percentage Burned Out":lambda m: self.calculate_percentage_burned(m)
            }
        )


        self.initialize_forest()

        # Start a random agglomeration of 4 trees on fire
        self.start_random_fire()

        self.running = True
        self.datacollector.collect(self)

    # CHANGED: Create and place trees based on selected spatial pattern 
    def initialize_forest(self):
        if self.spatial_pattern == "Random":
            self.place_trees_random()
        elif self.spatial_pattern == "Clustered":
            self.place_trees_clustered()
        elif self.spatial_pattern == "Lines":
            self.place_trees_lines()

    def place_trees_random(self):
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < self.density and self.grid.is_cell_empty((x, y)):
                new_tree = TreeCell((x, y), self)
                self.grid.place_agent(new_tree, (x, y))
                self.schedule.add(new_tree)

    def place_trees_clustered(self):
        cluster_size = 3  # Size of the cluster
        for i in range(0, self.width, cluster_size):
            for j in range(0, self.height, cluster_size):
                if self.random.random() < self.density:
                    for x in range(i, min(i + cluster_size, self.width)):
                        for y in range(j, min(j + cluster_size, self.height)):
                            if self.grid.is_cell_empty((x, y)):
                                new_tree = TreeCell((x, y), self)
                                self.grid.place_agent(new_tree, (x, y))
                                self.schedule.add(new_tree)

    def place_trees_lines(self):
        for x in range(0, self.width):  # Ensures every other column
            if self.random.random() < self.density:
                for y in range(self.height):
                    if self.grid.is_cell_empty((x, y)):
                        new_tree = TreeCell((x, y), self)
                        self.grid.place_agent(new_tree, (x, y))
                        self.schedule.add(new_tree)

    def start_random_fire(self):
        """
        Start a random agglomeration of 4 trees on fire.
        """
        fire_started = False
        while not fire_started:
            x = self.random.randint(0, self.grid.width - 2)
            y = self.random.randint(0, self.grid.height - 2)
            candidates = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
            if all(isinstance(self.grid[x, y], TreeCell) for x, y in candidates):
                for x, y in candidates:
                    tree = self.grid[x, y]
                    if tree and tree.condition == "Fine":
                        tree.condition = "On Fire"
                fire_started = True

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        percentage_burned = self.calculate_percentage_burned(self)
        #print(f"Step {self.schedule.time}: {percentage_burned:.2f}% Burned Out")

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False
            print("The fire has stopped.")
            results_df = self.datacollector.get_model_vars_dataframe()
            results_df.to_csv("results.csv", index = False)

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
    
    @staticmethod   
    def calculate_percentage_burned(model):
        """
        Helper method to calculate percentage of trees burned out 
        """
        total_trees = len(model.schedule.agents)
        burned_trees = sum(1 for agent in model.schedule.agents if agent.condition == "Burned Out")
        return (burned_trees / total_trees) * 100 if total_trees > 0 else 0

    
