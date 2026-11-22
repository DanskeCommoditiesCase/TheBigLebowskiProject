class BowlingGame:
    """Scoreboard for a single player's game of ten-pin bowling."""

    def __init__(self):
        self._rolls: list[int] = []

    def roll(self, pins: int) -> None:
        self._rolls.append(pins)

    def score(self) -> int:
        total_score = 0
        roll_index = 0
        for _ in range(10):
            frame_pins = self._rolls[roll_index] + self._rolls[roll_index + 1]
            if frame_pins == 10:
                total_score = total_score + 10 + self._rolls[roll_index + 2]
            else:
                total_score = total_score + frame_pins
            roll_index = roll_index + 2
        return total_score
