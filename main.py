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
    ga.set_max_generations(Mastermind.MAX_ATTEMPS)
    draw_generation = plot.plot_generation(generation=0)
    ga.set_plot(draw_generation)
    ga.run()

    # Mostrar la gráfica final
    plot.plt.show()

    print("\n###  SOLUTION ###\n")
    print("solution: ", ga.solution)


if __name__ == "__main__":
    main()
