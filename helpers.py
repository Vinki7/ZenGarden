import random

from solution import Solution


def crossover(parent1, parent2, gene_count):
    # Combine genes from two parents to create two child solutions
    half_point = gene_count // 2  # Integer division to find the midpoint

    parent1_genes = parent1[0].genes
    parent2_genes = parent2[0].genes

    # Create two offspring by swapping the halves of the parents' genes
    child1_genes = parent1_genes[:half_point] + parent2_genes[half_point:]
    child2_genes = parent2_genes[:half_point] + parent1_genes[half_point:]

    return [Solution(child1_genes), Solution(child2_genes)]

def uniform_crossover(parent1, parent2, gene_count):
    child1_genes, child2_genes = [], []

    for i in range(gene_count):
        if random.random() < 0.5:  # Randomly swap genes with 50% chance
            child1_genes.append(parent1[0].genes[i])
            child2_genes.append(parent2[0].genes[i])
        else:
            child1_genes.append(parent2[0].genes[i])
            child2_genes.append(parent1[0].genes[i])

    return [Solution(child1_genes), Solution(child2_genes)]


def select_n_random_solutions(population, n):
    population_size = len(population)

    selection = list()
    for _ in range(0, n):
        i = 0
        selected = population[random.randint(0, population_size - 1)]
        while selected[1] < 0 and i < population_size:
            selected = population[random.randint(0, population_size - 1)]
            i += 1

        selection.append(selected)

    return selection

def tournament_selection(population, tournament_size=3):
    # Select the best individuals using tournament selection
    selected = select_n_random_solutions(population, tournament_size)

    selected.sort(key=lambda x: x[1], reverse=True)

    return selected[0]

def roulette_selection(population, roulette_participant_count=10):
    # Select the best individuals using roulette selection
    individuals = select_n_random_solutions(population, roulette_participant_count)

    total_fitness = 0

    for solution in individuals:
        total_fitness += solution[1]

    cumulative_probabilities = []
    cumulative_sum = 0

    probabilities = list()

    for solution in individuals:
        probabilities.append(solution[1]/total_fitness)


    for prob in probabilities:
        cumulative_sum += prob
        cumulative_probabilities.append(cumulative_sum)

    rand_num = random.random()  # Generate a random number between 0 and 1
    for i, cumulative_prob in enumerate(cumulative_probabilities):
        if rand_num < cumulative_prob:
            return individuals[i]

def partition_selection(fitness_scores, population_size, selection_rate):
    number_of_individuals = int(population_size * selection_rate)
    return fitness_scores[:number_of_individuals]

def max_gene_count(garden_dimensions, rock_positions):
    return  garden_dimensions[0] + garden_dimensions[1] + len(rock_positions)

def max_value_in_gene(garden_dimensions):
    return  (garden_dimensions[0] + garden_dimensions[1]) * 2 # Whole perimeter


def extract_solution_from_tuple(group):
    for i in range(0, len(group)):
        tmp = group[i]
        group[i] = tmp[0]

    return group

def available_cell_count(dimensions, rock_positions):
    return dimensions[0] * dimensions[1] - len(rock_positions)