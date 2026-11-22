from bowling.game import BowlingGame, Frame
from tests.helpers import roll_spare, roll_strike


def test_unfinished_game_scores_completed_frames() -> None:
    game = BowlingGame()

    game.roll(3)
    game.roll(4)

    assert game.score() == 7


def test_half_finished_frame_is_not_scored_yet() -> None:
    game = BowlingGame()

    game.roll(3)
    game.roll(4)
    game.roll(5)

    assert game.score() == 7


def test_spare_waiting_for_bonus_is_not_scored_yet() -> None:
    game = BowlingGame()

    game.roll(3)
    game.roll(4)
    roll_spare(game)

    assert game.score() == 7


def test_strike_waiting_for_bonus_is_not_scored_yet() -> None:
    game = BowlingGame()

    game.roll(3)
    game.roll(4)
    roll_strike(game)
    game.roll(2)

    assert game.score() == 7


def test_frames_show_rolls_of_example_game() -> None:
    game = BowlingGame()

    for pins in [1, 4, 4, 5, 6, 4, 5, 5, 10, 0, 1, 7, 3, 6, 4, 10, 2, 8, 6]:
        game.roll(pins)

    rolls = [frame.rolls for frame in game.frames()]
    assert rolls == [
        (1, 4),
        (4, 5),
        (6, 4),
        (5, 5),
        (10,),
        (0, 1),
        (7, 3),
        (6, 4),
        (10,),
        (2, 8, 6),
    ]


def test_strike_waiting_for_bonus_shows_rolls_but_no_total() -> None:
    game = BowlingGame()

    game.roll(3)
    game.roll(4)
    roll_strike(game)

    assert game.frames() == [Frame((3, 4), 7), Frame((10,), None)]


def test_spare_waiting_for_bonus_shows_rolls_but_no_total() -> None:
    game = BowlingGame()

    game.roll(3)
    game.roll(4)
    roll_spare(game)

    assert game.frames() == [Frame((3, 4), 7), Frame((5, 5), None)]


def test_half_finished_frame_shows_its_roll() -> None:
    game = BowlingGame()

    game.roll(3)
    game.roll(4)
    game.roll(5)

    assert game.frames() == [Frame((3, 4), 7), Frame((5,), None)]
