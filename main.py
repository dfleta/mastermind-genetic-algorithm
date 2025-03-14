import matplotlib.pyplot as plt
from src.mastermind import Mastermind, Colors
from src.genetic_algorithm import Genetic


def guess_solution():
    solution = [Colors.RED, Colors.BLUE, Colors.PURPLE, Colors.YELLOW]
    game = Mastermind(solution)
    print(game.get_solution())

    pegs = (Colors.RED, Colors.BLUE, Colors.PURPLE, Colors.YELLOW)
    print(game.guess_solution(pegs))

    pegs = (Colors.BLACK, Colors.BLUE, Colors.PURPLE, Colors.YELLOW)
    print(game.guess_solution(pegs))

    solution = [Colors.RED, Colors.BLUE, Colors.PURPLE, Colors.RED]
    game = Mastermind(solution)
    pegs = (Colors.BLACK, Colors.BLUE, Colors.PURPLE, Colors.BLACK)
    print(game.guess_solution(pegs))

    solution = [Colors.RED, Colors.BLUE, Colors.PURPLE, Colors.YELLOW]
    game = Mastermind(solution)
    pegs = (Colors.BLUE, Colors.RED, Colors.YELLOW, Colors.PURPLE)
    print(game.guess_solution(pegs))

    solution = [Colors.RED, Colors.BLUE, Colors.YELLOW, Colors.BLUE]
    game = Mastermind(solution)
    pegs = (Colors.BLUE, Colors.RED, Colors.YELLOW, Colors.PURPLE)
    print(game.guess_solution(pegs))


def main():
    print("\n### GA ###\n")

    solution = [
        Colors.RED.name,
        Colors.BLUE.name,
        Colors.PURPLE.name,
        Colors.YELLOW.name,
    ]

    game = Mastermind(solution)
    print("\n### SOLUTION ###\n")
    print(game.get_solution())

    ga = Genetic()
    ga.set_fitness_function(game)

    ga.create_initial_population()
    print("\n### INITIAL POPULATION ###\n")
    print(ga.population)

    while not ga.stopping():
        ga.evaluate_population()
        print("\n### POPULATION FITNESS ###\n")
        print(ga.population_fitness)

        # Crear la gráfica de puntos
        plt.figure(figsize=(10, 6))
        chromosome_labels = [f"C{i + 1}" for i in range(len(ga.population))]
        plt.scatter(chromosome_labels, ga.population_fitness, color="blue", s=100)

        # Personalizar la gráfica
        plt.title("Fitness por Cromosoma")
        plt.xlabel("Cromosomas")
        plt.ylabel("Valor de Fitness")

        # Añadir los valores encima de cada punto
        for i, v in enumerate(ga.population_fitness):
            plt.text(i, v + 0.1, str(v), ha="center")

        # Conectar los puntos con una línea
        # plt.plot(chromosome_labels, ga.population_fitness, "b--", alpha=0.3)

        plt.grid(True, linestyle="--", alpha=0.7)
        plt.show()

        print("\n### PARENTS ###\n")
        parents_fitness = ga.select_parents()
        print("len parents: ", len(ga.parents))
        print(ga.parents)
        print("\n### PARENTS FITNESS ###\n")
        print(parents_fitness)

        ga.reproduce_offspring()
        print("\n###  OFFSPRING ###\n")
        print(ga.population)
        print("len population: ", len(ga.population))
        print("len parents: ", len(ga.parents))

        print("\n###  MUTATION  ###\n")
        ga.mutation()
        print("len population: ", len(ga.population))
        print("len parents: ", len(ga.parents))

        print("\n###  POPULATION SORTED ###\n")
        ga.populate_nex_generation()
        print("\n###  POPULATION SELECTED ###\n")
        print(ga.population)
        print("len population sorted: ", len(ga.population))

    print("\n###  SOLUTION ###\n")
    print("solution: ", ga.solution)


if __name__ == "__main__":
    main()
