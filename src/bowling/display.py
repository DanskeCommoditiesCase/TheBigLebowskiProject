"""Text scoreboard in bowling notation. Pure functions: no input or output."""

from bowling.game import FRAMES_PER_GAME, PINS_PER_FRAME, Frame

STRIKE = "X"
SPARE = "/"
MISS = "-"

FRAME_WIDTH = 5
LAST_FRAME_WIDTH = 7  # the 10th frame can hold three rolls


def roll_symbols(rolls: tuple[int, ...]) -> list[str]:
    """Bowling notation for one frame's rolls, for example (6, 4) -> ["6", "/"]."""
    symbols: list[str] = []
    first_ball: int | None = None  # pins from the first ball at the current set of pins
    for pins in rolls:
        if first_ball is None:
            symbols.append(STRIKE if pins == PINS_PER_FRAME else _count(pins))
            first_ball = None if pins == PINS_PER_FRAME else pins
        else:
            symbols.append(SPARE if first_ball + pins == PINS_PER_FRAME else _count(pins))
            first_ball = None
    return symbols


def render_scoreboard(frames: list[Frame]) -> str:
    """Three rows: frame numbers, rolls and running totals. Unknown totals are left blank."""
    widths = [FRAME_WIDTH] * (FRAMES_PER_GAME - 1) + [LAST_FRAME_WIDTH]
    numbers = [str(number) for number in range(1, FRAMES_PER_GAME + 1)]
    rolls = [" ".join(roll_symbols(frame.rolls)) for frame in frames]
    totals = ["" if frame.running_total is None else str(frame.running_total) for frame in frames]
    return "\n".join(
        [
            _row("Frame", numbers, widths),
            _row("Rolls", rolls, widths),
            _row("Total", totals, widths),
        ]
    )


def _count(pins: int) -> str:
    return MISS if pins == 0 else str(pins)


def _row(label: str, cells: list[str], widths: list[int]) -> str:
    cells = cells + [""] * (len(widths) - len(cells))
    boxes = "".join(f"{cell:^{width}}|" for cell, width in zip(cells, widths, strict=True))
    return f"{label} |{boxes}"
