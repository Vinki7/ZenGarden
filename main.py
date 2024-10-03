from garden import Garden
import config as cfg
from genetic_algorithm import GeneticAlgorithm


def main():
    # Initialize the garden
    garden = Garden(cfg.GARDEN_DIMENSION, cfg.ROCK_POSITIONS)

    # Initialize the genetic algorithm with the garden instance
    genetic_algorithm = GeneticAlgorithm(garden=garden,
                                         population_size=cfg.POPULATION_SIZE,
                                         max_generations=cfg.MAX_GENERATIONS,
                                         mutation_rate=cfg.MUTATION_RATE,
                                         uniform_partition_rate=cfg.UNIFORM_PARTITION_RATE,
                                         tournament_selection_size=cfg.TOURNAMENT_SELECTION_SIZE,
                                         best_selection=cfg.BEST_SELECTION_RATE,
                                         available_gene_percentage=cfg.AVAILABLE_GENE_COUNT_PERCENTAGE,
                                         stall_threshold=cfg.STALL_THRESHOLD,
                                         refresh_percentage = cfg.REFRESH_PERCENTAGE)

    # Run the genetic algorithm and get the best solution
    best_solution = genetic_algorithm.run()

    # Display the final raked garden
    garden.display_solution_map(best_solution)
    genetic_algorithm.describe_solution(best_solution)


if __name__ == "__main__":
    main()
