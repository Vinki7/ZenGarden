from config import BEST_SELECTION_RATE
from garden import Garden
import config as cfg
from genetic_algorithm import GeneticAlgorithm


def main():
    # Initialize the garden
    garden = Garden(cfg.GARDEN_DIMENSION, cfg.ROCK_POSITIONS)

    # Initialize the genetic algorithm with the garden instance
    genetic_algorithm = GeneticAlgorithm(garden, cfg.POPULATION_SIZE, cfg.MAX_GENERATIONS, cfg.MUTATION_RATE,
                                         cfg.BEST_SELECTION_RATE, cfg.AVAILABLE_GENE_COUNT_PERCENTAGE)

    # Run the genetic algorithm and get the best solution
    best_solution = genetic_algorithm.run()

    # Display the final raked garden
    garden.display_solution_map(best_solution)
    genetic_algorithm.describe_solution(best_solution)


if __name__ == "__main__":
    main()
