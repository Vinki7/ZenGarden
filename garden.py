import numpy as np

class Garden:
    def __init__(self, dimensions, rock_positions):
        self.dimensions = dimensions
        self.rock_positions = rock_positions
        self.grid = self._initialize_grid()

    def _initialize_grid(self):
        # Initialize the garden grid with rocks (-1) and empty cells (0)
        garden_grid =
        pass

    def generate_random_solutions(self):
        # Generate a random solution (genetic individual or chromosome)
        # Each solution can be a set of entry points on the perimeter and directional decisions
        pass

    def perimeter_points(self):
        # Return all points on the perimeter of the grid where the monk can start
        pass

    def evaluate_solution(self, solution):
        # Simulate the monk's path based on the solution and calculate coverage
        # Return the number of raked cells (fitness)
        pass

    def _rake(self, start_pont, direction, grid):
        # Simulate the raking process and return the number of cells covered
        # Logic to move monk based on direction and obstacles
        pass

    def display_solution(self, solution):
        # Display the final raked garden in a nice format
        pass