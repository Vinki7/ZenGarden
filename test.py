from garden import Garden
import config as cfg
from solution import Solution

garden = Garden(cfg.GARDEN_DIMENSION, cfg.ROCK_POSITIONS)

#garden.rake([0, 0], "D", garden.grid)
solution = Solution([37, 28, 4, 7, 11, 40, 43, 35, 13, 42, 31, 14, 16, 30, 38, 18, 44, 22, 34, 14, 10])

fitness = garden.evaluate_solution(solution)
print(f"Fitness: {fitness}")
print(solution.get_grid())
# genetic_algorithm.
# solution = Solution([1, 12,13, 22,23, 34,35, 44,1])
# for gene in solution.genes:
#
#     position = garden.starting_position(gene)
#
#     print(position, gene)