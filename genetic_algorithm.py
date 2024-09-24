import random

from chromosome import Chromosome
from helpers import max_gene_count, max_value_in_gene


def move(actual_position, direction):
    if direction == "D":
        return {actual_position[0], actual_position[1] + 1}

    if direction == "U":
        return {actual_position[0], actual_position[1] - 1}

    if direction == "L":
        return {actual_position[0] - 1, actual_position[1]}

    return {actual_position[0] + 1, actual_position[1]}

class GeneticAlgorithm:
    def __init__(self, garden, population_size, max_generations):
        self.garden = garden
        self.population_size = population_size
        self.max_generations = max_generations
        self.max_gene_count = max_gene_count(garden.dimensions, garden.rock_positions)
        self.population = self._initialize_population()

    def _initialize_population(self):
        # Create the initial population of random solutions (genetic individuals, chromosomes)
        chromosomes = list()

        for i in range(self.population_size):
            genes = list()
            for j in range(self.max_gene_count):
                new_starting_position = random.randint(1, max_value_in_gene(self.garden.dimensions))
                genes.append(new_starting_position)
            chromosomes.append(Chromosome(genes))
        return chromosomes

    def evaluate_fitness(self, chromosome):
        # Evaluate how much of the garden is covered by the monk's movements

        pass

    def run(self):
        # The core of the algorithm, every necessary part will be run here
        pass

    def starting_position_co_ords(self, gene_data):
        if gene_data <= self.garden.dimensions[0]:
            return { gene_data - 1, 0}

        return { 0, gene_data - 1}

