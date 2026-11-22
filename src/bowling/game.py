class BowlingGame:
    """Scoreboard for a single player's game of ten-pin bowling."""

    def roll(self, pins: int) -> None:
        raise NotImplementedError

    def score(self) -> int:
        raise NotImplementedError