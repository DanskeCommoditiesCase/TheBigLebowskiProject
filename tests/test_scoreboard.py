import pytest

from bowling.errors import InvalidRollError
from bowling.game import BowlingGame, Frame
from tests.helpers import roll_many, roll_spare, roll_strike


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


def test_new_game_is_not_complete() -> None:
    assert not BowlingGame().is_complete()


def test_game_is_complete_after_open_10th_frame() -> None:
    game = BowlingGame()

    roll_many(game, times=20, pins=0)

    assert game.is_complete()


def test_game_is_not_complete_while_10th_frame_spare_waits_for_bonus() -> None:
    game = BowlingGame()

    roll_many(game, times=18, pins=0)
    roll_spare(game)

    assert not game.is_complete()


def test_game_is_not_complete_while_10th_frame_strike_waits_for_bonus() -> None:
    game = BowlingGame()

    roll_many(game, times=18, pins=0)
    roll_strike(game)
    game.roll(5)

    assert not game.is_complete()


def test_game_is_complete_after_10th_frame_strike_and_two_bonus_rolls() -> None:
    game = BowlingGame()

    roll_many(game, times=18, pins=0)
    roll_strike(game)
    game.roll(5)
    game.roll(4)

    assert game.is_complete()


def test_game_is_complete_after_10th_frame_spare_and_bonus_roll() -> None:
    game = BowlingGame()

    roll_many(game, times=18, pins=0)
    roll_spare(game)
    game.roll(4)

    assert game.is_complete()


def test_perfect_game_is_complete() -> None:
    game = BowlingGame()

    roll_many(game, times=12, pins=10)

    assert game.is_complete()


def test_two_rolls_in_a_frame_cannot_exceed_10_pins() -> None:
    game = BowlingGame()
    game.roll(7)

    with pytest.raises(InvalidRollError):
        game.roll(7)


def test_rejected_roll_does_not_change_the_game() -> None:
    game = BowlingGame()
    game.roll(7)

    with pytest.raises(InvalidRollError):
        game.roll(7)
    game.roll(3)

    assert game.frames()[0].rolls == (7, 3)
