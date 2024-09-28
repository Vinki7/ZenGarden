from garden import Garden
import config as cfg
from solution import Solution

garden = Garden(cfg.GARDEN_DIMENSION, cfg.ROCK_POSITIONS)

solution = Solution([1, 12,13, 22,23, 34,35, 44,1])
for gene in solution.genes:

    position = garden.starting_position(gene)

    print(position, gene)