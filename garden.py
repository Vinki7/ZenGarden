import random

import numpy as np

class Garden:
    def __init__(self, dimensions, rock_positions):
        self.dimensions = dimensions
        self.rock_positions = rock_positions
        self.grid = self._initialize_grid()
        self._blocked_cell_flag = False
        self._out_of_grid = False

    def _initialize_grid(self):
        # Initialize the garden grid with rocks (-1) and empty cells (0)
        garden_grid = np.zeros((self.dimensions[1], self.dimensions[0]), dtype=int) # Rows, Columns
        for rock in self.rock_positions:
            garden_grid[rock[0], rock[1]] = -1
        return garden_grid

    def evaluate_solution(self, solution):
        # Simulate the monk's path based on the solution and calculate coverage
        # Return the number of raked cells (fitness)
        raked_cells = 0
        grid_copy = np.copy(self.grid)

        for gene in solution.genes:
            start_position = self.starting_position(gene)
            if not self._is_valid_position(start_position, grid_copy):
                continue

            raked_cells += self.rake(start_position, start_position[2], grid_copy, gene)
            if self._blocked_cell_flag:
                self._blocked_cell_flag = False
                solution.set_grid(grid_copy)
                return raked_cells

        solution.set_grid(grid_copy)
        return raked_cells

    def starting_position(self, gene_data):
        # Adjust for 1-based gene_data indexing if necessary
        gene_data -= 1

        t_edge = self.dimensions[0]
        r_edge = self.dimensions[1]

        max_row = t_edge - 1  # Last row index
        max_col = r_edge - 1  # Last column index

        # Top Edge: y = 0, x moves from 0 to max_col
        if gene_data < t_edge:
            return [gene_data, 0, "D"]

        # Right Edge: x = max_row, y moves from 1 to max_row
        gene_data -= t_edge
        if gene_data < r_edge:
            return [max_row, gene_data, "L"]

        # Bottom Edge: y = max_col, x moves from max_row to 0
        gene_data -= r_edge
        if gene_data < t_edge:
            return [max_row - gene_data, max_col, "U"]

        # Left Edge: x = 0, y moves from max_col to 0
        gene_data -= t_edge
        return [0, max_col - gene_data, "R"]

    def _is_valid_position(self, position, grid_copy):
        if position[0] < 0 or position[0] >= self.dimensions[0] or position[1] < 0 or position[1] >= self.dimensions[1]:
            return False

        return grid_copy[position[1], position[0]] == 0


    def rake(self, position, direction, grid, gene=1):
        # Simulate the raking process and return the number of cells covered
        # Logic to move monk based on direction and obstacles
        raked_cells = 0

        while self._is_valid_position(position, grid):
            grid[position[1]][position[0]] = gene
            raked_cells += 1
            position = self._move(position, direction, grid) # Check this part

            if self._blocked_cell_flag:
                return -100 # penalty
            if len(position) == 3:
                direction = position[2]
        return raked_cells


    @staticmethod
    def _is_valid_move(position, grid): # Check also this part and everything bellow
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

        potential_position = moves.get(direction)

        validation_result = self._is_valid_move(potential_position, grid)

        if validation_result == -1 or validation_result == 1:
            return potential_position

        return self._choose_new_direction(actual_position, direction, grid)

    def _choose_new_direction(self, position, direction, grid):
        # Try perpendicular directions first
        if direction in ["U", "D"]:
            return self._try_horizontal_move(position, direction, grid)
        else:
            return self._try_vertical_move(position, direction, grid)

    def _try_horizontal_move(self, position, direction, grid):
        # Try moving right first
        validation_result = self._is_valid_move([position[0] + 1, position[1]], grid)
        if validation_result == 1 or validation_result == -1:
            return [position[0] + 1, position[1], "R"]

        # Then try move left
        validation_result = self._is_valid_move([position[0] - 1, position[1]], grid)
        if validation_result == 1 or validation_result == -1:
            return [position[0] - 1, position[1], "L"]

        # If both directions are blocked or don't lead out of the grid, maintain the initial direction and raise a flag
        self._blocked_cell_flag = True
        return self._move_into_blocked_cell(position, direction)

    def _try_vertical_move(self, position, direction, grid):
        # Try moving up
        validation_result = self._is_valid_move([position[0], position[1] - 1], grid)
        if validation_result == 1 or validation_result == -1:
            return [position[0], position[1] - 1, "U"]

        #Tthen try moving down
        validation_result = self._is_valid_move([position[0], position[1] + 1], grid)
        if validation_result == 1 or validation_result == -1:
            return [position[0], position[1] + 1, "D"]

        # If both directions are blocked or don't lead out of the grid, maintain the initial direction and raise a flag
        self._blocked_cell_flag = True
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
    def display_solution_map(solution):
        # Display the final raked garden in a nice format
        print(solution[0].get_grid())
