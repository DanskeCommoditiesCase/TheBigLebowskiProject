class BowlingGame:
    """Scoreboard for a single player's game of ten-pin bowling."""

    def __init__(self):
        self._rolls: list[int] = []

    def roll(self, pins: int) -> None:
        self._rolls.append(pins)

    def score(self) -> int:
        return sum(self._rolls)
