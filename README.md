# The Big Lebowski Project: a bowling scoreboard

A scoreboard for a single player's game of ten-pin bowling, written in Python.
Roll by roll it shows each frame's pins and running total, just like the screen at a bowling alley.

```
Frame |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  10   |
Rolls | 1 4 | 4 5 | 6 / | 5 / |  X  | - 1 | 7 / | 6 / |  X  | 2 / 6 |
Total |  5  | 14  | 29  | 49  | 60  | 61  | 77  | 97  | 117 |  133  |
Score: 133
```

## Quick start

You need [uv](https://docs.astral.sh/uv/). It installs the right Python version and the locked dependencies.

```bash
git clone https://github.com/DanskeCommoditiesCase/TheBigLebowskiProject.git
cd TheBigLebowskiProject
uv sync

# Run the tests
uv run python -m pytest

# Score a list of rolls
uv run python -m bowling 1 4 4 5 6 4 5 5 10 0 1 7 3 6 4 10 2 8 6

# Or enter rolls one at a time, and watch the scoreboard update after each one
uv run python -m bowling
```

Without uv: `pip install -e .`, then `python -m bowling`.

An invalid roll is reported with its position, for example `Error in roll 2: Only 3 pins are standing, got 7`.
With rolls given as arguments the program then exits with code 1; in interactive mode it asks for the roll again.

## Design choices

**The rolls are the single source of truth.**
The game stores nothing but the list of rolls. Frames, frame scores and running totals are always calculated from that list.
There is no second copy of the state that could get out of sync, and the scoring logic is easy to test.

**A small public interface.**
`roll()`, `frames()`, `score()` and `is_complete()` are all that callers need.
`Frame` is a frozen dataclass holding a frame's rolls and its running total.
Everything else is private, so the internals can be refactored without breaking callers or tests.

**Unknown scores are `None`, not guesses.**
A strike or spare can't be scored until its bonus rolls are in.
Until then its running total is `None` and shown as an empty box, just like at a bowling alley.
Every later total is `None` as well, because it depends on the missing bonus.
`score()` returns the latest total that is known for certain.

**Invalid rolls are rejected before they are stored.**
`roll()` checks each roll before saving it, so a rejected roll never changes the game.
It raises `InvalidRollError` for:
- fewer than 0 or more than 10 pins
- more pins than are left standing, for example 7 then 7 in one frame, or 10, 5, 6 in the 10th frame

`InvalidRollError` inherits from `ValueError`, because a bad pin count is a bad value.

**The 10th frame needs no special scoring rule.**
A strike or spare in the 10th frame reads its bonus rolls like any other frame.
The bonus rolls belong to frame 10 instead of starting a frame 11, so they only count as bonus.
That is exactly the rule in the case description.

**Logic, display and input/output are kept apart.**
- `game.py` holds the rules.
- `display.py` turns frames into text using bowling notation (`X` strike, `/` spare, `-` miss), as pure functions.
- `__main__.py` is a thin command-line layer, and the only place that reads input or prints.

This "functional core, imperative shell" split means the rules can be reused anywhere, for example behind an API or in a data pipeline, without changes.

## Assumptions

- One player per game.
- Rolls arrive one at a time, in the order they were bowled.
- Python 3.12 or newer.

## Project structure

```
src/bowling/
  game.py        BowlingGame and Frame: the scoring rules
  errors.py      InvalidRollError
  display.py     Scoreboard rendering (pure functions)
  __main__.py    Command-line interface
tests/
  test_scoring.py      Scoring of complete games, including every example in the case
  test_scoreboard.py   Running totals, frames waiting for bonus rolls, is_complete, rejected rolls
  helpers.py           Small helpers such as roll_many and roll_strike
```

## How it was built and tested

The game logic was written test-first (TDD), in small red → green → refactor steps, and the commit history shows each step.

The tests cover:
- every example in the case description: the gutter game, the perfect game, both 10th-frame examples, and the full example game scoring 133
- one focused test per rule, such as spare bonus, strike bonus, frames waiting for bonus rolls and when a game is complete
- rejected rolls, and that a rejected roll leaves the game unchanged

The display module and the command-line interface are a thin layer on top of the tested game logic and have no tests of their own.

GitHub Actions runs the following on every push:
- linting with `ruff check`
- format checking with `ruff format --check`
- the test suite with `pytest`

Dependencies are managed with uv and locked in `uv.lock` for reproducible builds.

## Ideas for future work

- **Multiple players:** a `Match` holding one `BowlingGame` per player and tracking whose turn it is.
- **An API:** the core has no input/output, so a small HTTP API could sit on top of it without changing the rules.
- **Saving games:** storing the list of rolls is enough to rebuild any game, since everything else is calculated from it.

## Note on AI assistance

I used an AI assistant (Claude) as a pair-programming partner during this project.
It helped me discuss design options and review my code, and it drafted the command-line interface, the display module and this README.
I reviewed, tested and adjusted everything.
