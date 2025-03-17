from enum import Enum, unique
from colorama import init, Fore, Style

# Inicializar colorama
init()


@unique
class Colors(Enum):
    RED = (1, Fore.RED + "●" + Style.RESET_ALL)
    BLUE = (2, Fore.BLUE + "●" + Style.RESET_ALL)
    PURPLE = (3, Fore.MAGENTA + "●" + Style.RESET_ALL)
    YELLOW = (4, Fore.YELLOW + "●" + Style.RESET_ALL)
    GREEN = (5, Fore.GREEN + "●" + Style.RESET_ALL)
    WHITE = (6, Fore.WHITE + "●" + Style.RESET_ALL)
    BLACK = (7, Style.BRIGHT + Fore.BLACK + "●" + Style.RESET_ALL)


class Mastermind:
    MAX_ATTEMPS = 12

    def __init__(self, pegs):
        self.solution = tuple(pegs)

    def get_solution(self):
        return self.solution

    def guess_solution(self, pegs):
        # code = [0, 1, 1, -1]  0 blanco 1 negro -1 fallo
        code = [-1] * len(self.solution)
        used_pegs = set()
        for pos, peg in enumerate(pegs):
            if peg == self.solution[pos]:
                code[pos] = 1
                used_pegs.add(peg)
        # (P, R, G, W)  sol
        # (W, R, G, W)  guess

        for pos, peg in enumerate(pegs):
            if peg not in used_pegs:
                if self.solution.count(peg) > 0:
                    code[pos] = 0
                    used_pegs.add(peg)

        return code


def print_colored_solution(pegs):
    print("Solution: ", end="")
    for peg in pegs:
        if isinstance(peg, str):  # Si es un string (nombre del color)
            color = Colors[peg]
            print(color.value[1], end=" ")
        else:  # Si es un objeto Colors
            print(peg.value[1], end=" ")
    print()  # Nueva línea al final
