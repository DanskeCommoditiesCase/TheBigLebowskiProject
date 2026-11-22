from bowling.game import BowlingGame
from tests.helpers import roll_many, roll_spare, roll_strike

def test_gutter_game_scores_zero() -> None:
    game = BowlingGame()

    roll_many(game, times=20, pins=0)

    assert game.score() == 0


def test_all_ones_scores_twenty() -> None:
    game = BowlingGame()

    roll_many(game, times=20, pins=1)

    assert game.score() == 20


def test_spare_scores() -> None:
    game = BowlingGame()

    roll_spare(game)
    game.roll(3)  # bonus of spare

    roll_many(game, times=17, pins=0)

    assert game.score() == 16


def test_strike_scores() -> None:
    game = BowlingGame()

    roll_strike(game)
    game.roll(3)  # frame 2 roll 1
    game.roll(4)  # frame 2 roll 2

    roll_many(game, times=16, pins=0)

    assert game.score() == 24
