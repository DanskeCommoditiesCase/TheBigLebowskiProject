from bowling.game import BowlingGame


def test_gutter_game_scores_zero() -> None:
    game = BowlingGame()

    for _ in range(20):
        game.roll(0)

    assert game.score() == 0
