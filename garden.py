import random

import numpy as np

def make_decision(actual_position, direction):
    if direction == "D":
        pass

class Garden:
    def __init__(self, dimensions, rock_positions):
        self.dimensions = dimensions
        self.rock_positions = rock_positions
        self.t_edge = dimensions[0]
        self.t_r_edge = self.t_edge + dimensions[1]
        self.t_r_b_edge = self.t_r_edge + self.t_edge
        self.whole_perimeter = self.t_r_b_edge + self.t_edge
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
            start_position = self.starting_position(gene)
            if not self._is_valid_position(start_position):
                continue

            raked_cells += self._rake(start_position, start_position[2], grid_copy, gene)

        solution.set_grid(grid_copy)

        return raked_cells


    def starting_position(self, gene_data):
        # the math side explanation:
        # the -1 is due to the indexing of gene data (the len(x) is 12 but the maximal possible index is 11)
        dimensions = self.dimensions

        # On the TOP (x remains the same, y = 0)
        if gene_data <= self.t_edge:
            return [gene_data-1, 0, "D"]

        # On the right side (x = max, gene_data - top edge)
        if gene_data <= self.t_r_edge:
            return [dimensions[0] - 1, gene_data - dimensions[0] - 1, "L"]

        # On the bottom side (x = abs(gene_data - sum of top, right, and bottom edge len), y = max)
        if gene_data <= self.t_r_b_edge:
            return [abs(gene_data - self.t_r_b_edge), dimensions[1] - 1, "U"]

        # On the left side (x = 0, y = ?)
        return [0, self.whole_perimeter - gene_data - 2, "R"] # now only here is a problem with the math part---------


    def _is_valid_position(self, position):
        if position[0] < 0 or position[0] >= self.dimensions[0] or position[1] < 0 or position[1] >= self.dimensions[1]:
            return False

        return self.grid[position[1], position[0]] == 0


    def _rake(self, position, direction, grid, gene=1):
        # Simulate the raking process and return the number of cells covered
        # Logic to move monk based on direction and obstacles
        raked_cells = 0

        while self._is_valid_position(position):
            grid[position[1]][position[0]] = gene
            raked_cells += 1
            position = self._move(position, direction, grid)
            if len(position) == 3:
                direction = position[2]

        return raked_cells


    @staticmethod
    def _is_valid_move(position, grid):
        row = position[1]
        col = position[0]

        is_within_row_bounds = 0 <= row < len(grid)
        is_within_col_bounds = 0 <= col < len(grid[0])

        if is_within_col_bounds and is_within_row_bounds:
            if grid[row][col] == 0:
                return 1
            else:
                return 0

        return -1


    def _move(self, actual_position, direction, grid):
        # Define possible moves based on the current direction
        moves = {
            "D": [actual_position[0], actual_position[1] + 1],
            "U": [actual_position[0], actual_position[1] - 1],
            "L": [actual_position[0] - 1, actual_position[1]],
            "R": [actual_position[0] + 1, actual_position[1]]
        }

        next_position = moves.get(direction)
        is_valid = self._is_valid_move(next_position, grid)
        if is_valid == 1 or is_valid == -1:
            return next_position

        return self._choose_new_direction(actual_position, direction, grid)

    def _choose_new_direction(self, position, direction, grid):
        # Try perpendicular directions first
        if direction in ["U", "D"]:
            return self._try_horizontal_move(position, direction, grid)
        else:
            return self._try_vertical_move(position, direction, grid)

    def _try_horizontal_move(self, position, direction, grid):
        # Try moving right or left randomly
        if random.randint(0, 1):
            if self._is_valid_move([position[0] + 1, position[1]], grid):
                return [position[0] + 1, position[1], "R"]
            elif self._is_valid_move([position[0] - 1, position[1]], grid):
                return [position[0] - 1, position[1], "L"]
        else:
            if self._is_valid_move([position[0] - 1, position[1]], grid):
                return [position[0] - 1, position[1], "L"]
            elif self._is_valid_move([position[0] + 1, position[1]], grid):
                return [position[0] + 1, position[1], "R"]

        # If both directions are blocked, maintain the initial direction
        return self._move_into_blocked_cell(position, direction)

    def _try_vertical_move(self, position, direction, grid):
        # Try moving up or down randomly
        if random.randint(0, 1):
            if self._is_valid_move([position[0], position[1] - 1], grid):
                return [position[0], position[1] - 1, "U"]
            elif self._is_valid_move([position[0], position[1] + 1], grid):
                return [position[0], position[1] + 1, "D"]
        else:
            if self._is_valid_move([position[0], position[1] + 1], grid):
                return [position[0], position[1] + 1, "D"]
            elif self._is_valid_move([position[0], position[1] - 1], grid):
                return [position[0], position[1] - 1, "U"]

        # If both directions are blocked, maintain the initial direction
        return self._move_into_blocked_cell(position, direction)

    @staticmethod
    def _move_into_blocked_cell(position, direction):
        # Move into the blocked cell and return new position
        if direction == "D":
            return [position[0], position[1] + 1, direction]  # Continue down
        elif direction == "U":
            return [position[0], position[1] - 1, direction]  # Continue up
        elif direction == "L":
            return [position[0] - 1, position[1], direction]  # Continue left
        else:  # "R"
            return [position[0] + 1, position[1], direction]  # Continue right


    @staticmethod
    def display_solution(solution):
        # Display the final raked garden in a nice format
        print(solution.get_grid())
