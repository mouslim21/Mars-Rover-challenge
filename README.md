# Mars Rover Kata

Python solution to the **Mars Rover** kata: a squad of robotic rovers must explore a rectangular plateau on Mars, following movement instructions.

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

## Usage

```bash
python3 rover.py input.txt
```

### Example Output

```
1 3 N
5 1 E
```

## Project Structure

```
Mars-Rover-challenge/
├── README.md
├── rover.py       # Full solution (parsing + simulation)
└── input.txt      # Sample input file
```

## Boundary Behavior

If an `M` instruction would move a rover off the plateau, the move is simply ignored: the rover stays at its current position. Since the specification doesn't define this case explicitly, this choice was made to avoid undefined behavior.
