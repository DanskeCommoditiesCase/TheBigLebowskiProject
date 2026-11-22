"""Command-line scoreboard.

python -m bowling 1 4 4 5 10 ...   score the rolls given as arguments
python -m bowling                  enter rolls one at a time
"""

import sys

from bowling.display import render_scoreboard
from bowling.game import BowlingGame

USAGE = "usage: python -m bowling [PINS ...]"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if args and args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args:
        return _score_arguments(args)
    return _play_interactively()


def _score_arguments(args: list[str]) -> int:
    game = BowlingGame()
    for position, text in enumerate(args, start=1):
        try:
            _roll(game, text)
        except ValueError as error:
            print(f"Error in roll {position}: {error}", file=sys.stderr)
            print(USAGE, file=sys.stderr)
            return 1
    _show(game)
    return 0


def _play_interactively() -> int:
    game = BowlingGame()
    print("Enter the pins knocked down by each roll. Press Ctrl+C to stop.")
    while not game.is_complete():
        try:
            text = input("Pins: ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        try:
            _roll(game, text.strip())
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            continue
        _show(game)
    print(f"Game over. Final score: {game.score()}")
    return 0


def _roll(game: BowlingGame, text: str) -> None:
    """Parses one roll and adds it to the game. Raises ValueError for any bad input."""
    if game.is_complete():
        raise ValueError("The game is already over")
    try:
        pins = int(text)
    except ValueError:
        raise ValueError(f"{text!r} is not a whole number of pins") from None
    game.roll(pins)  # InvalidRollError is a ValueError too


def _show(game: BowlingGame) -> None:
    print(render_scoreboard(game.frames()))
    print(f"Score: {game.score()}")


if __name__ == "__main__":
    sys.exit(main())
