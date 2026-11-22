FRAMES_PER_GAME = 10
PINS_PER_FRAME = 10


class BowlingGame:
    """Scoreboard for a single player's game of ten-pin bowling."""

    def __init__(self) -> None:
        self._rolls: list[int] = []

    def roll(self, pins: int) -> None:
        self._rolls.append(pins)

    def score(self) -> int:
        total_score = 0
        frame_start = 0
        for _ in range(FRAMES_PER_GAME):
            if not self._has_rolls(frame_start, 1):
                break
            frame_score = self._frame_score(frame_start)
            if frame_score is None:
                break
            total_score = total_score + frame_score
            frame_start = frame_start + 1 if self._is_strike(frame_start) else frame_start + 2
        return total_score

    def _pins_in_frame(self, frame_start: int) -> int:
        return self._rolls[frame_start] + self._rolls[frame_start + 1]

    def _is_spare(self, frame_start: int) -> bool:
        return self._pins_in_frame(frame_start) == PINS_PER_FRAME

    def _spare_bonus(self, frame_start: int) -> int:
        return self._rolls[frame_start + 2]

    def _is_strike(self, frame_start: int) -> bool:
        return self._rolls[frame_start] == PINS_PER_FRAME

    def _strike_bonus(self, frame_start: int) -> int:
        return self._rolls[frame_start + 1] + self._rolls[frame_start + 2]

    def _has_rolls(self, frame_start: int, count: int) -> bool:
        return frame_start + count <= len(self._rolls)

    def _frame_score(self, frame_start: int) -> int | None:
        if self._is_strike(frame_start):
            if not self._has_rolls(frame_start, 3):
                return None
            return PINS_PER_FRAME + self._strike_bonus(frame_start)
        if not self._has_rolls(frame_start, 2):
            return None
        if self._is_spare(frame_start):
            if not self._has_rolls(frame_start, 3):
                return None
            return PINS_PER_FRAME + self._spare_bonus(frame_start)
        return self._pins_in_frame(frame_start)
