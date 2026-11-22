from dataclasses import dataclass

from bowling.errors import InvalidRollError

FRAMES_PER_GAME = 10
PINS_PER_FRAME = 10


@dataclass(frozen=True)
class Frame:
    """One frame on the scoreboard: the pins rolled and the total so far."""

    rolls: tuple[int, ...]
    running_total: int | None  # None until the frame's bonus rolls are known


class BowlingGame:
    """Scoreboard for a single player's game of ten-pin bowling."""

    def __init__(self) -> None:
        self._rolls: list[int] = []

    def roll(self, pins: int) -> None:
        if not 0 <= pins <= PINS_PER_FRAME:
            raise InvalidRollError(f"A roll must knock down 0-{PINS_PER_FRAME} pins, got {pins}")
        standing = self._pins_standing()
        if pins > standing:
            raise InvalidRollError(f"Only {standing} pins are standing, got {pins}")
        self._rolls.append(pins)

    def score(self) -> int:
        known_totals = [f.running_total for f in self.frames() if f.running_total is not None]
        return known_totals[-1] if known_totals else 0

    def frames(self) -> list[Frame]:
        frames: list[Frame] = []
        running_total: int | None = 0
        frame_start = 0
        for frame_number in range(1, FRAMES_PER_GAME + 1):
            if not self._has_rolls(frame_start, 1):
                break
            frame_score = self._frame_score(frame_start)
            if running_total is None or frame_score is None:
                running_total = None
            else:
                running_total += frame_score
            size = self._frame_size(frame_start, frame_number)
            rolls = tuple(self._rolls[frame_start : frame_start + size])
            frames.append(Frame(rolls, running_total))
            frame_start += size
        return frames

    def is_complete(self) -> bool:
        frames = self.frames()
        if len(frames) < FRAMES_PER_GAME:
            return False
        last_rolls = frames[-1].rolls
        if len(last_rolls) == 3:
            return True
        return len(last_rolls) == 2 and sum(last_rolls) < PINS_PER_FRAME

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

    def _frame_size(self, frame_start: int, frame_number: int) -> int:
        if frame_number == FRAMES_PER_GAME:
            return len(self._rolls) - frame_start
        return 1 if self._is_strike(frame_start) else 2

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

    def _pins_standing(self) -> int:
        frames = self.frames()
        if not frames:
            return PINS_PER_FRAME
        rolls = frames[-1].rolls
        if len(frames) < FRAMES_PER_GAME:
            if len(rolls) == 1 and rolls[0] < PINS_PER_FRAME:
                return PINS_PER_FRAME - rolls[0]
            return PINS_PER_FRAME
        pins_down = 0
        for pins in rolls:
            pins_down += pins
            if pins_down == PINS_PER_FRAME:
                pins_down = 0
        return PINS_PER_FRAME - pins_down
