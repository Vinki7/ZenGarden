class Chromosome:
    def __init__(self, genes):
        self.gene = genes
        self.fitness_eval = 0

    def set_fitness_eval(self, fitness_eval):
        self.fitness_eval = fitness_eval