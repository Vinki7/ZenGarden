import random

from chromosome import Chromosome
from helpers import max_gene_calculator


class GeneticAlgorithm:
    def __init__(self, garden, population_size, max_generations):
        self.garden = garden
        self.population_size = population_size
        self.max_generations = max_generations
        self.max_gene_count = max_gene_calculator(garden.dimensions, garden.rock_positions)
        self.population = self._initialize_population()

    def _initialize_population(self):
        # Create the initial population of random solutions (genetic individuals, chromosomes)
        chromosomes = list()

        for i in range(self.population_size):
            genes = list()
            for j in range(self.max_gene_count):
                genes.append(random.randint(1, self.max_gene_count))
            chromosomes.append(Chromosome(genes))
        # stacked on the logical part here... I need to figure out the usage of the dict or maybe the usage of the class, just let's think it out
        return chromosomes

    def evaluate_fitness(self, solution):
        # Evaluate how much of the garden is covered by the monk's movements
        pass

    def run(self):
        # The core of the algorithm, every necessary part will be run here
        pass

