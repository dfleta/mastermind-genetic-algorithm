from src.mastermind import Colors
import random


class Genetic:
    POPULATION_SIZE = 60
    PARENTS_SIZE = 40  # 20 parejas generan 2 hijos por pareja = 40, total poblacion 60 + 40 => matar a ¿?
    F_MAX_GLOBAL = 4

    def __init__(self):
        self.population = set()
        self.population_fitness = []
        self.parents = []
        self.solution = ()
        self.max_generations = 0

    def generate_chromosome(self):
        # cambiar a choice para que haya replacemnt y elegir mas de una vez un color
        return random.sample(list(Colors.__members__.keys()), 4)

    def create_initial_population(self):
        while len(self.population) < Genetic.POPULATION_SIZE:
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
        # choices = list(zip(self.population, self.population_fitness))
        # roulette wheel selection
        self.parents = [
            self.weighted_random_choice(choices) for _ in range(Genetic.PARENTS_SIZE)
        ]
        return [self.evaluate_individual(parent) for parent in self.parents]

    def weighted_random_choice(self, choices):
        max = sum([fitness + Genetic.F_MAX_GLOBAL for _, fitness in choices])
        pick = random.uniform(0, max)
        current = 0
        for chromosome, fitness in choices:
            current += fitness + Genetic.F_MAX_GLOBAL
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
        MUTATION_RATIO = Genetic.POPULATION_SIZE // 10
        for _ in range(MUTATION_RATIO):
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
        # [((Chromosoma), fitness)]
        choices = [
            (chromosome, self.evaluate_individual(chromosome))
            for chromosome in self.population
        ]
        # elitism selection
        sorted_by_fitness = sorted(choices, key=lambda item: item[1], reverse=True)
        return set(
            [chromosome for chromosome, _ in sorted_by_fitness][
                : Genetic.POPULATION_SIZE
            ]
        )

    def rank_selection(self):
        chromosomes = list(self.population)
        population_fitness = list(map(self.evaluate_individual, chromosomes))
        population_fitness = list(map(lambda fitness: fitness + 4, population_fitness))
        selected_individuals = set()
        while len(selected_individuals) < Genetic.POPULATION_SIZE:
            selected_individuals.add(
                random.choices(chromosomes, weights=population_fitness, k=1)[0]
            )
        assert len(selected_individuals) == Genetic.POPULATION_SIZE
        return selected_individuals

    def stopping(self):
        return self.global_maximum()

    def global_maximum(self):
        global_maximum = set(
            filter(
                lambda chromosome: self.evaluate_individual(chromosome)
                == Genetic.F_MAX_GLOBAL,
                self.population,
            )
        )
        if global_maximum:
            self.solution = global_maximum.pop()
            return self.solution
        else:
            return ()

    def set_plot(self, draw_function):
        self.draw_generation = draw_function

    def run(self):
        ### INITIAL POPULATION ###
        self.create_initial_population()

        attemps = 0
        while not self.stopping() and attemps < self.max_generations:
            ### POPULATION FITNESS ###
            self.evaluate_population()

            ### SELECT PARENTS ###
            parents_fitness = self.select_parents()

            ###  REPRODUCE OFFSPRING ###
            self.reproduce_offspring()

            ###  MUTATION  ###
            self.mutation()

            ###  SELECT POPULATION by ELITISM or RANK WHEEL ###
            self.populate_nex_generation()

            attemps += 1

            ### PLOT GENERATION FITNESS ###
            self.draw_generation(len(self.population), self.population_fitness)
