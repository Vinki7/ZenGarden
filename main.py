from config import BEST_SELECTION_RATE
from garden import Garden
import config as cfg
from genetic_algorithm import GeneticAlgorithm


def main():
    # Initialize the garden
    garden = Garden(cfg.GARDEN_DIMENSION, cfg.ROCK_POSITIONS)

    # Initialize the genetic algorithm with the garden instance
    genetic_algorithm = GeneticAlgorithm(garden, cfg.POPULATION_SIZE, cfg.MAX_GENERATIONS, cfg.MUTATION_RATE,
                                         cfg.GENETIC_SELECTION_RATE, BEST_SELECTION_RATE)

    # Run the genetic algorithm and get the best solution
    best_solution = genetic_algorithm.run()

    # Display the final raked garden
    garden.display_solution(best_solution)


if __name__ == "__main__":
    main()
