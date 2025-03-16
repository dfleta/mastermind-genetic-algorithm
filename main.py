import matplotlib.pyplot as plt
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

    # Crear una única figura fuera del bucle que se reutilizará
    plt.figure(figsize=(10, 6))

    # Lista de colores para cada generación
    colors = [
        "blue",
        "red",
        "green",
        "purple",
        "orange",
        "brown",
        "pink",
        "gray",
        "cyan",
        "magenta",
    ]
    generation = 0

    while not ga.stopping():
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

        # Obtener color para esta generación
        color = colors[generation % len(colors)]

        # Crear la gráfica de puntos para esta generación
        chromosome_labels = [f"{i + 1}" for i in range(len(ga.population))]
        plt.scatter(
            chromosome_labels,
            ga.population_fitness,
            color=color,
            s=100,
            label=f"Generación {generation}",
        )

        # Añadir los valores encima de cada punto
        for i, v in enumerate(ga.population_fitness):
            plt.text(i, v + 0.1, str(v), ha="center", color=color)

        # Personalizar la gráfica
        plt.title("Fitness por Cromosoma - Evolución de Generaciones")
        plt.xlabel("Cromosomas")
        plt.ylabel("Valor de Fitness")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()

        # Mostrar la gráfica actualizada
        plt.draw()
        plt.pause(1)  # Pausa breve para ver la actualización

        generation += 1

    # Mostrar la gráfica final
    plt.show()

    print("\n###  SOLUTION ###\n")
    print("solution: ", ga.solution)


if __name__ == "__main__":
    main()
