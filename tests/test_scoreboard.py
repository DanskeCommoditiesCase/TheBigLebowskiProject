from bowling.game import BowlingGame
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


def test_running_totals_match_example_from_case() -> None:
    game = BowlingGame()

    for pins in [1, 4, 4, 5, 6, 4, 5, 5, 10, 0, 1, 7, 3, 6, 4, 10, 2, 8, 6]:
        game.roll(pins)

    assert game.running_totals() == [5, 14, 29, 49, 60, 61, 77, 97, 117, 133]
