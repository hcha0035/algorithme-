# N-Puzzle Solver in Python

A command-line solver for the **N-puzzle** (sliding-tile puzzle), written in pure Python.

The program reads an `N × N` board from a CSV file, checks whether the configuration is solvable, searches for a sequence of legal moves, and writes the solution to a text file.

## Features

- Supports square sliding puzzles of arbitrary size (`3×3`, `4×4`, and more)
- Reads and validates puzzle boards from CSV files
- Represents the empty tile with `x`
- Detects unsolvable configurations using inversion parity
- Generates legal moves dynamically from the current board state
- Uses recursive depth-limited search with backtracking
- Stores visited states in a dictionary to avoid redundant exploration
- Allows a configurable maximum number of moves
- Writes the resulting move sequence to a text file
- Uses only the Python standard library

## Project Structure

```text
.
├── solve_puzzle.py   # Search algorithm and command-line entry point
├── utils.py          # Board parsing, validation, moves, and solvability checks
└── README.md
```

## Requirements

- Python **3.9+**
- No third-party dependencies

## Input Format

The input must be a square CSV file.

- Each numbered tile is represented by an integer.
- The empty tile is represented by `x`.
- There must be exactly one empty tile.
- Numbered tiles must not be duplicated.

Example `board.csv`:

```csv
1,2,3
4,5,6
7,x,8
```

The target configuration is generated automatically:

```text
1 2 3
4 5 6
7 8 x
```

For an `N × N` puzzle, the goal contains the values `1` through `N² - 1`, followed by the empty tile in the bottom-right corner.

## Usage

```bash
python solve_puzzle.py <input_csv> <output_file> [max_steps]
```

### Arguments

| Argument | Description |
|---|---|
| `input_csv` | Path to the CSV file containing the initial board |
| `output_file` | Path where the solution sequence will be written |
| `max_steps` | Optional maximum search depth; defaults to `40` |

### Example

```bash
python solve_puzzle.py board.csv solution.txt 20
```

For the example board above, `solution.txt` contains:

```text
D
```

This means that the empty tile must move one position to the right.

## Move Encoding

The project uses French initials for the movement of the empty tile:

| Code | French | English |
|---|---|---|
| `G` | Gauche | Left |
| `D` | Droite | Right |
| `H` | Haut | Up |
| `B` | Bas | Down |

A solution such as:

```text
DDBGH
```

represents a sequence of five moves applied from left to right.

## How It Works

### 1. Board parsing and validation

`utils.read_board_csv()`:

- reads the CSV file;
- checks that the board is square;
- converts `x` to `None`;
- rejects invalid tile values;
- verifies that there is exactly one empty tile;
- rejects duplicate numbered tiles.

### 2. Solvability test

Before starting the search, the program counts inversions in the flattened board.

- For an odd board width, the puzzle is solvable when the inversion count is even.
- For an even board width, solvability also depends on the empty tile's row counted from the bottom.

This avoids searching configurations that can never reach the target state.

### 3. State representation

Boards are converted from mutable lists into tuples of tuples:

```python
tuple(tuple(row) for row in board)
```

This immutable representation can be used as a dictionary key.

The search history records the smallest depth at which each state has been reached. A state is explored again only when the new path is shorter than the previously recorded one.

### 4. Recursive search

The solver performs a depth-limited depth-first search:

1. Compare the current board with the goal.
2. Stop if the maximum depth has been reached.
3. Generate all legal moves.
4. Apply each move to create a new board.
5. Skip states already reached through an equal or shorter path.
6. Continue recursively.
7. Backtrack when a branch does not produce a solution.

The first solution found within the depth limit is returned.

## Algorithmic Complexity

Let:

- `b` be the average branching factor;
- `d` be the maximum search depth.

The worst-case time complexity is approximately:

```text
O(b^d)
```

The visited-state dictionary reduces repeated work, but the number of possible puzzle configurations still grows rapidly.

The solver is therefore best suited to:

- small puzzles;
- boards close to the goal;
- educational demonstrations of state-space search and backtracking.

It may be slow on difficult `4×4` instances.

## Important Limitation

The current depth-first search returns the **first solution found**. It does not guarantee the shortest possible solution.

For guaranteed shortest paths or better performance, possible replacements include:

- Breadth-First Search for small puzzles
- Iterative Deepening Depth-First Search
- A* search with Manhattan distance
- IDA* for larger state spaces
- Bidirectional search

## Possible Improvements

- Use A* with a Manhattan-distance heuristic
- Use iterative deepening to find shorter solutions
- Avoid immediately applying the inverse of the previous move
- Add `argparse` for clearer command-line options
- Add unit tests with `pytest`
- Add performance benchmarks
- Validate that the numbered tiles exactly match `1 ... N² - 1`
- Add a graphical or terminal visualization
- Improve error messages in the command-line interface
- Add continuous integration with GitHub Actions

## Skills Demonstrated

This project demonstrates:

- recursive algorithms;
- backtracking;
- graph and state-space search;
- memoization with hashable state representations;
- algorithmic pruning;
- combinatorial solvability conditions;
- file parsing and validation;
- command-line application design;
- Python type annotations;
- modular software organization.

## AI-Assistance Disclosure

Some comments and portions of the utility code were produced with assistance from ChatGPT and subsequently reviewed and adapted for educational purposes by the author.

## Author

**Hamza Chamaoui**

Mathematics student interested in algorithms, probability, and quantitative problem solving.
