from src.mastermind import Colors, print_colored_pegs
import random


class GA:
    POPULATION_SIZE = 60
    PARENTS_SIZE = 40  # 20 parejas generan 2 hijos por pareja = 40, total poblacion 60 + 40 => matar a ¿?
    F_MAX_GLOBAL = 4
    MUTATION_RATIO = (POPULATION_SIZE + PARENTS_SIZE) // 10

    def __init__(self):
        self.population = set()
        self.population_fitness = []
        self.parents = []
        self.solution = ()
        self.max_generations = 0
        self.maximum_locals = set()

    def generate_chromosome(self):
        # cambiar a choice para que haya replacemnt y elegir mas de una vez un color
        return random.sample(list(Colors.__members__.keys()), 4)

    def create_initial_population(self):
        while len(self.population) < GA.POPULATION_SIZE:
            # set() no permite duplicados => chromosomas unicos
            self.population.add(tuple(self.generate_chromosome()))

    def set_fitness_function(self, game):
        self.fitness_function = game

    def set_max_generations(self, num_max_generations):
        self.max_generations = num_max_generations

    def evaluate_individual(self, chromosome):
        return sum(self.fitness_function.guess_solution(chromosome))

    def evaluate_population(self):
        self.population_fitness = list(map(self.evaluate_individual, self.population))

    def select_parents(self):
        # los cromosomas en el set son unicos
        choices = [
            (chromosome, self.evaluate_individual(chromosome))
            for chromosome in self.population
        ]
        # roulette wheel selection
        self.parents = [
            self.weighted_random_choice(choices) for _ in range(GA.PARENTS_SIZE)
        ]

    def weighted_random_choice(self, choices):
        max = sum([fitness + GA.F_MAX_GLOBAL for _, fitness in choices])
        pick = random.uniform(0, max)
        current = 0
        for chromosome, fitness in choices:
            current += fitness + GA.F_MAX_GLOBAL
            if current > pick:
                return chromosome

    def reproduce_offspring(self):
        while len(self.parents) >= 2:
            parent_a, parent_b = random.sample(self.parents, k=2)
            child_a, child_b = self.single_point_crossover(parent_a, parent_b)
            self.population.add(child_a)
            self.population.add(child_b)
            self.parents.remove(parent_a)
            self.parents.remove(parent_b)

    def single_point_crossover(self, parent_a, parent_b, gen_position=2):
        child_a = parent_a[:gen_position] + parent_b[gen_position:]
        child_b = parent_b[:gen_position] + parent_a[gen_position:]
        return child_a, child_b

    def mutation(self):
        for _ in range(GA.MUTATION_RATIO):
            if len(self.parents) > 0:
                chromosome = self.parents.pop()
            else:
                chromosome = random.choice(tuple(self.population))
                self.population.remove(chromosome)

            gen_muted = random.randrange(0, len(chromosome))
            muted = list(chromosome)
            muted[gen_muted] = random.choice(list(Colors.__members__.keys()))
            self.population.add(tuple(muted))

    def populate_nex_generation(self):
        # self.population = self.elitism_selection()
        self.population = self.rank_selection()
        self.population_fitness = list(map(self.evaluate_individual, self.population))

    def elitism_selection(self):
        sorted_by_fitness = self._sorted_chromosome_by_fitness()
        return set(
            [chromosome for chromosome, _ in sorted_by_fitness][
                : GA.POPULATION_SIZE
            ]
        )

    def _sorted_chromosome_by_fitness(self):
        # [((Chromosoma), fitness)]
        choices = [
            (chromosome, self.evaluate_individual(chromosome))
            for chromosome in self.population
        ]
        return sorted(choices, key=lambda item: item[1], reverse=True)

    def rank_selection(self):
        chromosomes = list(self.population)
        population_fitness = list(map(self.evaluate_individual, chromosomes))
        population_fitness = list(map(lambda fitness: fitness + 4, population_fitness))
        selected_individuals = set()
        while len(selected_individuals) < GA.POPULATION_SIZE:
            selected_individuals.add(
                random.choices(chromosomes, weights=population_fitness, k=1)[0]
            )
        return selected_individuals

    def stopping(self):
        return self.solution if self.global_maximum() else self.local_maximum()
        # self.solution = self.global_maximum() if self.global_maximum() else self.local_maximum()

    def global_maximum(self):
        global_maximum = set(
            filter(
                lambda chromosome: self.evaluate_individual(chromosome)
                == GA.F_MAX_GLOBAL,
                self.population,
            )
        )
        if global_maximum:
            self.solution = global_maximum.pop()
        return self.solution

    def local_maximum(self):
        local_maximums = self._sorted_chromosome_by_fitness()
        best_chromosome = local_maximums.pop(0)
        while best_chromosome in self.maximum_locals:
            best_chromosome = local_maximums.pop(0)
        self.maximum_locals.add(best_chromosome)
        return ()

    def set_plot(self, draw_function):
        self.draw_generation = draw_function

    def run(self):
        ### INITIAL POPULATION ###
        self.create_initial_population()

        attemps = 0
        ### STOP CONDITION ###
        while not self.stopping() and attemps < self.max_generations:
            ### POPULATION FITNESS ###
            self.evaluate_population()

            ### SELECT PARENTS ###
            self.select_parents()

            ###  REPRODUCE OFFSPRING ###
            self.reproduce_offspring()

            ###  MUTATION  ###
            self.mutation()

            ###  SELECT POPULATION by ELITISM or RANK WHEEL ###
            self.populate_nex_generation()

            attemps += 1

            ### PLOT GENERATION FITNESS ###
            self.draw_generation(len(self.population), self.population_fitness)
