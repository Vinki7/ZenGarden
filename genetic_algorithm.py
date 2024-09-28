import random
from audioop import reverse

from solution import Solution
from helpers import max_gene_count, max_value_in_gene

class GeneticAlgorithm:
    def __init__(self, garden, population_size, max_generations, mutation_rate, genetic_selection, best_selection):
        self.garden = garden
        self.population_size = population_size
        self.max_generations = max_generations
        self.max_gene_count = max_gene_count(garden.dimensions, garden.rock_positions)
        self.mutation_rate = mutation_rate
        self.genetic_selection = genetic_selection
        self.best_selection = best_selection
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
        fitness_scores = list()
        for solution in self.population:
            fitness_scores.append((solution, self.evaluate_fitness(solution)))

        fitness_scores.sort(key=lambda x: x[1], reverse=True) # Sort by fitness descending

        best_solution = fitness_scores[0][0]
        best_fitness = fitness_scores[0][1]
        print(f"Generation --placeholder--: Best fitness = {best_fitness}")

        return best_solution

#    def _genetic_operations_selection(self, fitness_scores):
#        return fitness_scores[:self.population_size * self.selection_rate]

#    def _select_best_solution(self, fitness_scores):
#        return fitness_scores[:self.population_size * (self.selection_rate])