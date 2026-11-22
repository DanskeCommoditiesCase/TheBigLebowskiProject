from bowling.game import BowlingGame


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
