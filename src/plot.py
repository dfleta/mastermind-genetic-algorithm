import matplotlib.pyplot as plt

# Crear una única figura fuera del bucle que se reutilizará
plt.figure(figsize=(10, 6))

# Lista de colores para cada generación
COLORS = [
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
            "lime",
            "teal"
        ]

def plot_generation(generation=0):

    def draw_generation(population_size, population_fitness):

        nonlocal generation
        # Obtener color para esta generación
        color = COLORS[generation % len(COLORS)]

        # Crear la gráfica de puntos para esta generación
        chromosome_labels = [f"{i + 1}" for i in range(population_size)]
        plt.scatter(
            chromosome_labels,
            population_fitness,
            color=color,
            s=100,
            label=f"Generación {generation}",
        )

        # Añadir los valores encima de cada punto
        for i, v in enumerate(population_fitness):
            plt.text(i, v + 0.1, str(v), ha="center", color=color)

        # Personalizar la gráfica
        plt.title("Fitness por Cromosoma - Evolución de Generaciones")
        plt.xlabel("Cromosomas")
        plt.ylabel("Valor de Fitness")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()

        # Mostrar la gráfica actualizada
        plt.draw()
        plt.pause(2)  # Pausa breve para ver la actualización

        generation += 1

    return draw_generation
