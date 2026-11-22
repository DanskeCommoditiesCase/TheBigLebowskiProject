from bowling.game import BowlingGame


def test_gutter_game_scores_zero() -> None:
    game = BowlingGame()

    for _ in range(20):
        game.roll(0)

    assert game.score() == 0


def test_all_ones_scores_twenty() -> None:
    game = BowlingGame()

    for _ in range(20):
        game.roll(1)

    assert game.score() == 20

def test_spare_scores() -> None:
    game = BowlingGame()

    game.roll(5)
    game.roll(5) #spare
    game.roll(3) #bonus of spare

    for _ in range(17):  
        game.roll(0)

    assert game.score() == 16
