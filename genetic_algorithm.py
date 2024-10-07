import random
import matplotlib.pyplot as plt

from solution import Solution
from helpers import max_gene_count, max_value_in_gene, partition_selection, crossover, tournament_selection, \
    roulette_selection, extract_solution_from_tuple, available_cell_count, uniform_crossover


class GeneticAlgorithm:
    def __init__(self, garden, population_size, max_generations, mutation_rate, uniform_partition_rate, tournament_selection_size, best_selection, stall_threshold, refresh_percentage, available_gene_percentage):
        self.garden = garden
        self.population_size = population_size
        self.max_generations = max_generations
        self.max_gene_count = int(max_gene_count(garden.dimensions, garden.rock_positions) * available_gene_percentage)
        self.mutation_rate = mutation_rate
        self.uniform_partition_rate = uniform_partition_rate
        self.tournament_selection_size = tournament_selection_size
        self.best_selection_rate = best_selection
        self.stall_threshold = stall_threshold
        self.refresh_percentage = refresh_percentage
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

        # Setup plotting
        plt.ion()  # Turn on interactive mode
        fig, ax = plt.subplots()
        line, = ax.plot([], [], lw=2)

        plt.title('Fitness Trend Over Generations')
        plt.xlabel('Generations')
        plt.ylabel('Fitness')

        ax.set_xlim(0, self.max_generations)
        ax.set_ylim(0, 114)

        fitness_scores = []
        best_fitness_trend = []

        config_adjusted = False

        no_of_generation = 1
        generations_since_last_improvement = 0
        generation_refreshment_count = 0

        current_best_fitness = 0
        best_solution = None
        best_fitness = 0

        while no_of_generation <= self.max_generations and best_fitness < self.max_fitness:
            if generations_since_last_improvement > self.stall_threshold and self.refresh_percentage != 0:
                num_to_remove = int(self.population_size * self.refresh_percentage)
                self.population = self.population[:-num_to_remove]
                self.population.extend(self.refresh_population())
                print(f"{int(self.refresh_percentage * 100)} % of population was refreshed")
                generations_since_last_improvement = 0
                generation_refreshment_count += 1
                if not config_adjusted and no_of_generation > 800: # prev best = 800
                    self.adjust_configurations()
                    config_adjusted = True

            for solution in self.population:
                fitness_scores.append((solution, self.evaluate_fitness(solution)))

            fitness_scores.sort(key=lambda x: x[1], reverse=True) # Sort by fitness descending

            best_solution_tuple = fitness_scores[0]
            best_solution = best_solution_tuple[0]
            best_fitness = best_solution_tuple[1]
            best_fitness_trend.append(best_fitness)

            if current_best_fitness < best_fitness:
                generations_since_last_improvement = 0
            else:
                generations_since_last_improvement += 1


            best_solutions = partition_selection(fitness_scores, self.population_size, self.best_selection_rate)
            best_solutions = extract_solution_from_tuple(best_solutions)

            cross_over_selection = partition_selection(fitness_scores, self.population_size, 1-self.best_selection_rate)

            offsprings = self.get_offsprings(cross_over_selection)

            mutate_group = self.mutate_group(offsprings, self.mutation_rate)

            self.population.clear()
            self.population.extend(best_solutions)
            self.population.extend(mutate_group)

            print(f"Generation {no_of_generation}: Best fitness = {best_fitness}")
            no_of_generation += 1
            current_best_fitness = best_fitness

            # Update plot
            line.set_xdata(range(len(best_fitness_trend)))
            line.set_ydata(best_fitness_trend)
            ax.set_xlim(0, no_of_generation + 1)

            plt.draw()  # Redraw the chart
            plt.pause(0.01)  # Short pause for the GUI to update

        plt.ioff()  # Turn off interactive mode
        plt.show()

        return tuple([best_solution, best_fitness])

    def get_offsprings(self, source):
        uniform = list()
        multi_point = list()
        offsprings = list()

        source_len = len(source)
        uniform_limit = int(source_len * self.uniform_partition_rate)
        multi_point_limit = source_len - uniform_limit

        counter = 1

        while len(uniform) < uniform_limit or len(multi_point) < multi_point_limit:
            parent_1 = tournament_selection(source, self.tournament_selection_size)
            parent_2 = roulette_selection(source)

            if (counter % 2 == 0) and len(uniform) < uniform_limit:
                # Perform uniform crossover
                uniform.extend(uniform_crossover(parent_1, parent_2, self.max_gene_count))
            elif len(multi_point) < multi_point_limit:
                # Perform single-point crossover
                multi_point.extend(crossover(parent_1, parent_2, self.max_gene_count))

            counter += 1  # Ensure counter is explicitly incremented

        offsprings.extend(uniform)
        offsprings.extend(multi_point)

        return offsprings

    def mutate_group(self, offsprings, mutation_rate):
        for offspring in offsprings:
            for i in range(len(offspring.genes)):
                if random.random() < mutation_rate:
                    offspring.genes[i] = random.randint(1, max_value_in_gene(self.garden.dimensions))
        return offsprings

    def refresh_population(self):
        new_population_part = []

        for _ in range(int(self.population_size * self.refresh_percentage)):
            genes = list()
            for j in range(self.max_gene_count):
                new_starting_position = random.randint(1, max_value_in_gene(self.garden.dimensions))
                genes.append(new_starting_position)
            new_population_part.append(Solution(genes))
        return new_population_part

    def describe_solution(self, solution):
        print(f"The best solution is: {solution[0].genes}\n"
              f"\t- Fitness: {solution[1]}\n"
              f"Settings:\n"
              f"\t- Maximum number of genes for each solution: {self.max_gene_count}\n"
              f"\t- Population size: {self.population_size}\n"
              f"\t- Maximum number of generations: {self.max_generations}\n"
              f"\t- Maximum fitness possible: {self.max_fitness}\n"
              f"\t- Percentage of the best solutions brought to new generation: {int(self.best_selection_rate*100)}%\n"
              f"\t- Mutation rate: {int(self.mutation_rate*100)}%\n"
              f"\t- Uniform cross-over percentage: {int(self.uniform_partition_rate*100)}%")

    @staticmethod
    def plot_fitness_trend(fitness_trend):
        plt.figure(figsize=(10, 6))
        plt.plot(fitness_trend, label="Best Fitness")
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.title('Fitness Trend Over Generations')
        plt.legend()
        plt.grid(True)
        plt.show()

    def adjust_configurations(self):
        self.mutation_rate = self.mutation_rate*0.75
        self.refresh_percentage *= 1.25
        self.tournament_selection_size = 2
        self.stall_threshold *= 0.5
