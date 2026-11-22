from bowling.game import BowlingGame


def roll_many(game: BowlingGame, times: int, pins: int) -> None:
    for _ in range(times):
        game.roll(pins)


def roll_spare(game: BowlingGame) -> None:
    game.roll(5)
    game.roll(5)


def roll_strike(game: BowlingGame) -> None:
    game.roll(10)
