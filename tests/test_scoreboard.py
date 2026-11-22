from bowling.game import BowlingGame


def test_unfinished_game_scores_completed_frames() -> None:
    game = BowlingGame()

    game.roll(3)
    game.roll(4)

    assert game.score() == 7
