from garden import Garden
import config as cfg
from genetic_algorithm import GeneticAlgorithm


def main():
    # Initialize the garden
    garden = Garden(cfg.GARDEN_DIMENSION, cfg.ROCK_POSITIONS)
    # Initialize the genetic algorithm with the garden instance
    genetic_algorithm = GeneticAlgorithm(garden, cfg.POPULATION_SIZE, cfg.MAX_GENERATIONS)

    # Run the genetic algorithm
    # Display the results
    print(garden.grid)
    for chromosome in genetic_algorithm.population:
        print(chromosome.genes)

if __name__ == "__main__":
    main()