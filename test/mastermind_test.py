from src.mastermind import Colors, Mastermind
import pytest


@pytest.fixture(name="game")
def setup():
    solution = [Colors.RED, Colors.BLUE, Colors.PURPLE, Colors.YELLOW]
    game = Mastermind(solution)
    return game


def test_solution_list_to_tuple_init(game):
    assert game.get_solution() == (
        Colors.RED,
        Colors.BLUE,
        Colors.PURPLE,
        Colors.YELLOW,
    )


def test_guess_solution(game):

    pegs = (Colors.RED, Colors.BLUE, Colors.PURPLE, Colors.YELLOW)
    assert game.guess_solution(pegs) == [1, 1, 1, 1]

    pegs = (Colors.BLACK, Colors.BLUE, Colors.PURPLE, Colors.YELLOW)
    assert game.guess_solution(pegs) == [-1, 1, 1, 1]

    solution = [Colors.RED, Colors.BLUE, Colors.PURPLE, Colors.RED]
    game = Mastermind(solution)
    pegs = (Colors.BLACK, Colors.BLUE, Colors.PURPLE, Colors.BLACK)
    assert game.guess_solution(pegs) == [-1, 1, 1, -1]

    solution = [Colors.RED, Colors.BLUE, Colors.PURPLE, Colors.YELLOW]
    game = Mastermind(solution)
    pegs = (Colors.BLUE, Colors.RED, Colors.YELLOW, Colors.PURPLE)
    assert game.guess_solution(pegs) == [0, 0, 0, 0]

    solution = [Colors.RED, Colors.BLUE, Colors.YELLOW, Colors.BLUE]
    game = Mastermind(solution)
    pegs = (Colors.BLUE, Colors.RED, Colors.YELLOW, Colors.PURPLE)
    assert game.guess_solution(pegs) == [0, 0, 1, -1]
