import random

from solution import Solution
from helpers import max_gene_count, max_value_in_gene

class GeneticAlgorithm:
    def __init__(self, garden, population_size, max_generations):
        self.garden = garden
        self.population_size = population_size
        self.max_generations = max_generations
        self.max_gene_count = max_gene_count(garden.dimensions, garden.rock_positions)
        self.population = self._initialize_population()

    def _initialize_population(self):
        # Create the initial population of random solutions (genetic individuals, chromosomes)
        population = list()

        for _ in range(self.population_size):
            genes = list()
            for j in range(self.max_gene_count):
                new_starting_position = random.randint(1, max_value_in_gene(self.garden.dimensions))
                genes.append(new_starting_position)
            population.append(Solution(genes))
        return population

    def evaluate_fitness(self, solution):
        # Evaluate how much of the garden is covered by the monk's movements
        return self.garden.evaluate_solution(solution)

    def run(self):
        # The core of the algorithm, every necessary part will be run here
        for solution in self.population:
            solution.fitness_eval = self.evaluate_fitness(solution)

        return self.population[0]