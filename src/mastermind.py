from enum import Enum, unique


@unique
class Colors(Enum):
    RED = 1
    BLUE = 2
    PURPLE = 3
    YELLOW = 4
    GREEN = 5
    WHITE = 6
    BLACK = 7


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
