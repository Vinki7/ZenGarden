import numpy as np
from numpy.random import poisson


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
        garden_grid = np.zeros((self.dimensions[1], self.dimensions[0]), dtype=int) # Columns, Rows

        # Add rocks
        for rock in self.rock_positions:
            garden_grid[rock[0], rock[1]] = -1

        return garden_grid

    def evaluate_solution(self, solution):
        # Simulate the monk's path based on the solution and calculate coverage
        # Return the number of raked cells (fitness)

        grid_copy = self.grid
        raked_cells = 0

        for gene in solution.genes:
            start_position = self._starting_position(gene)
            if not self._is_valid_position(start_position):
                continue

            raked_cells += self._rake(start_position, start_position[2], grid_copy, gene)

        return raked_cells


    def _starting_position(self, gene_data):
        gene_data -= 1
        dimensions = self.dimensions

        if gene_data in range(0, self.top_edge_len):
            return [gene_data, 0, "D"]

        if gene_data in range(self.top_edge_len, self.right_edge_len):
            return [dimensions[0] - 1, gene_data, "L"]

        if gene_data in range(self.right_edge_len, self.bottom_edge_len):
            return [gene_data, dimensions[1] - 1, "U"]

        return [0, gene_data, "R"]

    @staticmethod
    def _move(actual_position, direction):
        # Move the monk based on the current direction
        direction = direction

        if direction == "D":
            return [actual_position[0], actual_position[1] + 1]
        elif direction == "U":
            return [actual_position[0], actual_position[1] - 1]
        elif direction == "L":
            return [actual_position[0] - 1, actual_position[1]]
        else:  # "R" case
            return [actual_position[0] + 1, actual_position[1]]

    def _is_valid_position(self, position):
        if position[0] < 0 or position[0] >= self.dimensions[1] or position[1] < 0 or position[1] >= self.dimensions[0]:
            return False

        return self.grid[position[0], position[1]] == 0


    def _rake(self, position, direction, grid, gene=1):
        # Simulate the raking process and return the number of cells covered
        # Logic to move monk based on direction and obstacles
        raked_cells = 0

        while self._is_valid_position(position):
            grid[position[0]][position[1]] = gene
            raked_cells += 1
            position = self._move(position, direction)

        return raked_cells

    def display_solution(self, solution):
        # Display the final raked garden in a nice format
        grid_copy = self.grid
        raked_cells = 0

        for gene in solution.genes:
            start_position = self._starting_position(gene)
            if not self._is_valid_position(start_position):
                continue

            raked_cells += self._rake(start_position, start_position[2], grid_copy)

        print(grid_copy)
