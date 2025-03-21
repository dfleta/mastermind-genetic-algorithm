import src.plot as plot
from src.mastermind import Mastermind, Colors, print_colored_pegs
from src.genetic_algorithm import GA


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

    ga = GA()
    ga.set_fitness_function(game)
    ga.set_max_generations(Mastermind.MAX_ATTEMPS)
    draw_generation = plot.plot_generation(generation=0)
    ga.set_plot(draw_generation)

    ga.run()

    # Mostrar la gráfica final
    plot.plt.show()

    print("\n### LOCALS ###\n")
    for peg, fitness in ga.maximum_locals:
        print_colored_pegs(peg)
        print(fitness)
    print("\n###  SOLUTION ###\n")
    print_colored_pegs(ga.solution)
    print("\n")


if __name__ == "__main__":
    main()
