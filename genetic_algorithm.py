import random
from os import rename

from solution import Solution
from helpers import max_gene_count, max_value_in_gene, partition_selection, crossover, tournament_selection, \
    roulette_selection, extract_solution_from_tuple, available_cell_count


class GeneticAlgorithm:
    def __init__(self, garden, population_size, max_generations, mutation_rate, best_selection, available_gene_percentage):
        self.garden = garden
        self.population_size = population_size
        self.max_generations = max_generations
        self.max_gene_count = int(max_gene_count(garden.dimensions, garden.rock_positions) * available_gene_percentage)
        self.mutation_rate = mutation_rate
        self.best_selection_rate = best_selection
        self.max_fitness = available_cell_count(garden.dimensions, garden.rock_positions)
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

        no_of_generation = 1

        best_solution = None
        best_fitness = 0

        while no_of_generation <= self.max_generations and best_fitness < self.max_fitness:
            for solution in self.population:
                fitness_scores.append((solution, self.evaluate_fitness(solution)))

            fitness_scores.sort(key=lambda x: x[1], reverse=True) # Sort by fitness descending

            best_solution = fitness_scores[0][0]
            best_fitness = fitness_scores[0][1]

            best_solutions = partition_selection(fitness_scores, self.population_size, self.best_selection_rate)
            best_solutions = extract_solution_from_tuple(best_solutions)

            cross_over_selection = partition_selection(fitness_scores, self.population_size, 1-self.best_selection_rate)

            offsprings = self.get_offsprings(cross_over_selection)
            offsprings = extract_solution_from_tuple(offsprings)

            mutate_group = self.mutate_group(offsprings, self.mutation_rate)

            self.population.clear()
            self.population.extend(best_solutions)
            self.population.extend(mutate_group)

            print(f"Generation {no_of_generation}: Best fitness = {best_fitness}")
            no_of_generation += 1

        return tuple([best_solution, best_fitness])

    def get_offsprings(self, source):
        offsprings = list()
        while len(offsprings) < len(source):
            parent_1 = tournament_selection(source)
            parent_2 = roulette_selection(source)
            offsprings.append(crossover(parent_1, parent_2, self.max_gene_count))

        return offsprings

    def mutate_group(self, offsprings, mutation_rate):
        for offspring in offsprings:
            for i in range(len(offspring.genes)):
                if random.random() < mutation_rate:
                    offspring.genes[i] = random.randint(1, max_value_in_gene(self.garden.dimensions))
        return offsprings

    def describe_solution(self, solution):
        print(f"The best solution is: {solution[0].genes}\n"
              f"\t- Fitness: {solution[1]}\n"
              f"\t- Settings:\n"
              f"\t- Maximum number of genes for each solution: {self.max_gene_count}\n"
              f"\t- Population size: {self.population_size}\n"
              f"\t- Maximum number of generations: {self.max_generations}\n"
              f"\t- Maximum fitness possible: {self.max_fitness}\n"
              f"\t- Percentage of the best solutions brought to new generation: {int(self.best_selection_rate*100)}%\n"
              f"\t- Mutation rate: {int(self.mutation_rate*100)}%\n")

