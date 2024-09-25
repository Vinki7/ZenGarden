import random

def crossover(parent1, parent2):
    # Combine genes from two parents to create a child solution
    pass

def mutate(child, mutation_rate=0.1):
    # Randomly mutate a child's genes with some probability
    pass

def tournament_selection(population, tournament_size=3):
    # Select the best individuals using tournament selection
    pass

def roulette_selection(population, roulette_participant_count=3):
    # Select the best individuals using roulette selection
    pass

def max_gene_count(garden_dimensions, rock_positions):
    return  garden_dimensions[0] + garden_dimensions[1] + len(rock_positions)

def max_value_in_gene(garden_dimensions):
    return  (garden_dimensions[0] + garden_dimensions[1]) * 2 # Whole perimeter