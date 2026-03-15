# MazeGen

MazeGen is a reusable Python maze generator module providing deterministic and customizable maze generation.
It supports multiple generation algorithms and exposes the maze structure and its shortest solution path.

The module is designed to be reused in other Python projects.

---

# Installation

After building the package, install it using pip:

```
pip install mazegen-1.0.0-py3-none-any.whl
```

or directly from source:

```
pip install .
```

---

# Basic Usage

```python
from mazegen import MazeGenerator

config = {
    "WIDTH": 20,
    "HEIGHT": 20,
    "ENTRY": (0, 0),
    "EXIT": (19, 19),
    "PERFECT": True,
    "ALGORITHM": "dfs",
    "SEED": 42
}

generator = MazeGenerator(config)

maze = generator.generate_maze()

print("Maze grid:")
print(maze["grid"])

print("Shortest path:")
print(maze["path"])
```

---

# Configuration Parameters

The generator is instantiated using a configuration dictionary.

| Parameter | Type           | Description                               |
| --------- | -------------- | ----------------------------------------- |
| WIDTH     | int            | Width of the maze                         |
| HEIGHT    | int            | Height of the maze                        |
| ENTRY     | tuple(int,int) | Entry cell coordinates                    |
| EXIT      | tuple(int,int) | Exit cell coordinates                     |
| PERFECT   | bool           | If True the maze has a single solution    |
| ALGORITHM | str            | Maze generation algorithm (`dfs` or `bt`) |
| SEED      | int (optional) | Random seed for reproducibility           |

Example:

```
config = {
    "WIDTH": 30,
    "HEIGHT": 30,
    "ENTRY": (0, 0),
    "EXIT": (29, 29),
    "PERFECT": False,
    "ALGORITHM": "dfs",
    "SEED": 123
}
```

---

# Accessing the Maze Structure

The `generate_maze()` method returns a dictionary containing:

| Key        | Description                            |
| ---------- | -------------------------------------- |
| grid       | Internal maze grid representation      |
| entry      | Entry cell                             |
| exit       | Exit cell                              |
| path       | Shortest path from entry to exit       |
| pattern_42 | Cells used to display the `42` pattern |

Example:

```
maze = generator.generate_maze()

grid = maze["grid"]
entry = maze["entry"]
exit = maze["exit"]
path = maze["path"]
```

The grid uses a **bitmask wall representation**:

```
1 = North wall
2 = East wall
4 = South wall
8 = West wall
```

---

# Solving the Maze

The generator automatically computes the shortest path using **Breadth-First Search (BFS)**.

The path is returned as a string composed of:

```
N  -> move north
E  -> move east
S  -> move south
W  -> move west
```

Example output:

```
EESSSEENNWW
```

---

# Algorithms

The module currently supports two generation algorithms:

### Depth-First Search (DFS)

Backtracking algorithm producing long corridors and complex mazes.

```
ALGORITHM = "dfs"
```

### Binary Tree

Fast algorithm generating directional mazes.

```
ALGORITHM = "bt"
```

---

# Special Feature: 42 Pattern

If the maze size allows it, a **"42" pattern** is embedded in the center of the maze.

If the maze is too small, the pattern is omitted and a warning message is displayed.

---

# Example Output

Example grid representation:

```
[15, 11, 10, 14]
[13, 1, 4, 12]
[7, 2, 8, 3]
```

Each number represents the walls surrounding the cell using the bitmask format.

---
