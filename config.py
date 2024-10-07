# Configurable parameters for the genetic algorithm
POPULATION_SIZE = 400 # for now 300 is the best performing
MAX_GENERATIONS = 3000 # for now 2000
MUTATION_RATE = 0.7 # for now 0.7
BEST_SELECTION_RATE = 0.01

TOURNAMENT_SELECTION_SIZE = 3 # 2 was the previous optimal number
UNIFORM_PARTITION_RATE = 0.4 # 0.4 might be the optimal This represents the part of solutions which are to perform uniform crossover

STALL_THRESHOLD = 250 # number of generations with unchanged maximum fitness 250/50
REFRESH_PERCENTAGE = 0.50 # 30 may be sufficient

# Zen garden configuration
GARDEN_DIMENSION = (12, 10) # Columns (x), Rows (y)
ROCK_POSITIONS = [(1, 5), (2, 1), (3, 4), (4, 2), (6, 8), (6, 9)]

AVAILABLE_GENE_COUNT_PERCENTAGE = 0.7 # Sub-optimal is 0.75 or 0.6

#max score = 114