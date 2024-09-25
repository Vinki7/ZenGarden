import numpy as np
from numpy.random import poisson


def move(actual_position, direction):
    if direction == "D":
        return [actual_position[0], actual_position[1] + 1]

    if direction == "U":
        return [actual_position[0], actual_position[1] - 1]

    if direction == "L":
        return [actual_position[0] - 1, actual_position[1]]

    return [actual_position[0] + 1, actual_position[1]]

def make_decision(actual_position, direction):
    if direction == "D":
        pass

class Garden:
    def __init__(self, dimensions, rock_positions):
        self.dimensions = dimensions
        self.rock_positions = rock_positions
        self.top_edge_len = dimensions[0]
        self.right_edge_len = self.top_edge_len + dimensions[1]
        self.bottom_edge_len = self.right_edge_len + self.top_edge_len
        self.left_edge_len = self.bottom_edge_len + self.right_edge_len
        self.grid = self._initialize_grid()

    def _initialize_grid(self):
        # Initialize the garden grid with rocks (-1) and empty cells (0)
        # Create the grid initialized to 0
        garden_grid = np.zeros((self.dimensions[0], self.dimensions[1]), dtype=int)

        # Add rocks
        for rock in self.rock_positions:
            garden_grid[rock[0], rock[1]] = -1

        return garden_grid

    def evaluate_solution(self, solution):
        # Simulate the monk's path based on the solution and calculate coverage
        # Return the number of raked cells (fitness)

        raked_cells = 0

        for gene in solution.genes:
            position = self._starting_position_co_ords(gene)
            if not self._position_validation(position):
                continue

            self.grid[position[0]][position[1]] = gene

            while True:
                position = move(position, position[2])
                if not self._position_validation(position):
                    make_decision(position, position[2])



        return raked_cells

        pass

    def _starting_position_co_ords(self, gene_data):
        gene_data -= 1
        dimensions = self.dimensions

        if gene_data in range(0, self.top_edge_len):
            return [gene_data, 0, "D"]

        if gene_data in range(self.top_edge_len, self.right_edge_len):
            return [dimensions[0] - 1, gene_data, "L"]

        if gene_data in range(self.right_edge_len, self.bottom_edge_len):
            return [gene_data, dimensions[1] - 1, "U"]

        return [0, gene_data, "R"]

    def _position_validation(self, position):
        grid_field = self.grid[position[0]][position[1]]

        if grid_field == -1:
            return False

        if grid_field != 0:
            return False

        return True


    def _rake(self, start_pont, direction, grid):
        # Simulate the raking process and return the number of cells covered
        # Logic to move monk based on direction and obstacles
        pass

    def display_solution(self, solution):
        # Display the final raked garden in a nice format
        pass
