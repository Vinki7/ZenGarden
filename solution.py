class Solution:
    def __init__(self, genes):
        self._grid = None
        self.genes = genes

    def set_grid(self, grid):
        self._grid = grid

    def get_grid(self):
        return self._grid