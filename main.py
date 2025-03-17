import src.plot as plot
from src.mastermind import Mastermind, Colors
from src.genetic_algorithm import Genetic


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

    draw_generation = plot.plot_generation(generation=0)

    attemps = 0
    while not ga.stopping() and attemps < Mastermind.MAX_ATTEMPS:
        ga.evaluate_population()
        print("\n### POPULATION FITNESS ###\n")
        print(ga.population_fitness)

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

        attemps += 1

        draw_generation(len(ga.population), ga.population_fitness)


    # Mostrar la gráfica final
    plot.plt.show()

    print("\n###  SOLUTION ###\n")
    print("solution: ", ga.solution)


if __name__ == "__main__":
    main()
