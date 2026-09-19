# Mars Rover Kata

Python solution to the **Mars Rover** kata: a squad of robotic rovers must explore a rectangular plateau on Mars, following movement instructions sent by NASA.

## Problem Description

A rover is defined by:
- A position `(x, y)` on a grid
- A cardinal direction: `N`, `S`, `E`, or `W`

Instructions sent to a rover are a string made up of:
- `L`: turn 90° left (without moving)
- `R`: turn 90° right (without moving)
- `M`: move forward one grid point in the current direction

Rovers are processed **sequentially**: the next rover doesn't start moving until the previous one has finished all its instructions.

## Input File Format

```
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

- The first line gives the upper-right coordinates of the plateau (the lower-left corner is always `0 0`).
- Each rover is described by two lines: its starting position/direction, followed by its instruction string.

## How It Works

### Turning (`L` / `R`)

The four cardinal directions are stored in a fixed, clockwise order:

```python
DIRECTIONS = ["N", "E", "S", "W"]
```

Turning is just moving an index forward or backward in this list, with wraparound:
- `R` (turn right) → move **forward** one position in the list (`index + 1`)
- `L` (turn left) → move **backward** one position in the list (`index - 1`)

The modulo operator (`% 4`) handles the wraparound automatically — e.g. turning right from `W` (index 3) goes to index `0`, which is `N`.

```python
def tourner(direction, commande):
    index = DIRECTIONS.index(direction)
    if commande == "L":
        index = (index - 1) % 4
    elif commande == "R":
        index = (index + 1) % 4
    return DIRECTIONS[index]
```

This avoids a long, error-prone chain of `if/elif` statements for every direction/turn combination.

### Moving (`M`)

Each direction has a fixed `(dx, dy)` offset, stored in a lookup table:

```python
MOVES = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}
```

Moving forward simply adds the offset for the current direction to the current position. Before applying the move, the new position is checked against the plateau boundaries `[0, max_x] x [0, max_y]`. If the move would leave the plateau, it is **ignored** and the rover stays in place — the kata specification doesn't define this case explicitly, so this choice was made to avoid undefined behavior.

### Iterative vs. Recursive Implementation

Two implementations of the instruction-execution logic are included in `rover.py`, to compare the two approaches:

- **`deplacer_rover`** (iterative) — loops over each character of the instruction string with a simple `for` loop.
- **`deplacer_rover_recursif`** (recursive, kept for comparison) — processes the first instruction, then recurses on the rest of the string until it's empty (base case).

**The iterative version is the one actually used** (in `resoudre()`), for these reasons:
- **Memory**: the iterative version uses constant memory; the recursive version adds one stack frame per instruction character, which could hit Python's recursion limit (~1000 by default) on very long instruction strings.
- **Performance**: no per-character function-call overhead.
- **No tail-call optimization in Python**: unlike some other languages, Python does not optimize recursive tail calls, so the recursive version's stack usage is real, not free.
- **Fit for the problem**: the instructions form a simple, flat sequence with no natural recursive/tree-like structure, so a loop is the more natural and idiomatic tool here.

Both functions are tested to produce identical results for the same input.

## Usage

### Option 1: Run locally by cloning the repo

```bash
git clone https://github.com/mouslim21/Mars-Rover-challenge.git
cd Mars-Rover-challenge
python3 rover.py input.txt
```

Expected output:
```
1 3 N
5 1 E
```

### Option 2: Let the CI pipeline run it for you

This repository includes a GitHub Actions workflow (`.github/workflows/test.yml`) that automatically runs the program against `input.txt` and verifies the output matches the expected result, on every push and pull request to `main`.

To see it run:
1. Go to the **Actions** tab of this repository on GitHub.
2. Select the latest **Tests** workflow run to view the logs and result (✅ or ❌).
3. The workflow can also be triggered manually via the **"Run workflow"** button, thanks to the `workflow_dispatch` trigger.

## Project Structure

```
Mars-Rover-challenge/
├── .github/
│   └── workflows/
│       └── test.yml     # CI pipeline: runs rover.py and checks the output
├── README.md
├── rover.py             # Full solution (parsing + simulation)
└── input.txt            # Sample input file
```

## Boundary Behavior

If an `M` instruction would move a rover off the plateau, the move is simply ignored: the rover stays at its current position. Since the specification doesn't define this case explicitly, this choice was made to avoid undefined behavior.