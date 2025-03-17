import src.plot as plot
from src.mastermind import Mastermind, Colors, print_colored_pegs
from src.genetic_algorithm import Genetic


def main():
    solution = [
        Colors.RED.name,
        Colors.BLUE.name,
        Colors.GREEN.name,
        Colors.YELLOW.name,
    ]

    game = Mastermind(solution)
    print("\n### CODE ###\n")
    print_colored_pegs(game.get_solution())
    print()
    print("\n### LOCALS ###\n")

    ga = Genetic()
    ga.set_fitness_function(game)
    ga.set_max_generations(Mastermind.MAX_ATTEMPS)
    draw_generation = plot.plot_generation(generation=0)
    ga.set_plot(draw_generation)

    ga.run()

    # Mostrar la gráfica final
    plot.plt.show()

    print("\n###  SOLUTION ###\n")
    print_colored_pegs(ga.solution)
    print()


if __name__ == "__main__":
    main()
