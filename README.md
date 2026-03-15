*This project has been created as part of the 42 curriculum by onaanaa, aakourya.*

#  A-Maze-ing

---

## Description

**A-Maze-ing** is a maze generation and solving project built in Python as part of the 42 school curriculum. The goal is to programmatically generate mazes of configurable dimensions, embed a special **"42" pattern** at the center, solve them using BFS (Breadth-First Search), and display them interactively in the terminal using emoji-based rendering.

The project supports:
- Two maze generation algorithms: **DFS (Depth-First Search)** and **Binary Tree**
- Optional **imperfect mazes** (with loops/cycles)
- **BFS-based pathfinding** from entry to exit
- **Interactive terminal UI** with path toggling and wall color themes
- Configurable entry/exit points, grid dimensions, and random seed

---

## Instructions

### Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

### Installation

```bash
make install
```

### Running the Project

```bash
make run
```

This will run the program with the default `config.txt` file. You can also run it manually:

```bash
python3 a_maze_ing.py config.txt
```

### Interactive Controls

Once launched, the program displays the maze and presents a menu:

```
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Change maze wall colours
4. Quit
```

### Other Makefile Targets

| Command | Description |
|---|---|
| `make install` | Install Python dependencies |
| `make run` | Run the maze generator with `config.txt` |
| `make debug` | Run with Python debugger (pdb) |
| `make clean` | Remove `__pycache__` and `.mypy_cache` |
| `make lint` | Run `flake8` + `mypy` checks |
| `make lint-strict` | Run `mypy` in strict mode |

---

## Config File Structure

The configuration file uses a simple `KEY=VALUE` format. Lines beginning with `#` are treated as comments and ignored.

```ini
# ====== mandatory ===========
WIDTH=30
HEIGHT=30
ENTRY=10,16
EXIT=10,12
OUTPUT_FILE=out.txt
PERFECT=True

# ====== additional keys =======
ALGORITHM=dfs
SEED=8
```

### Config Keys

| Key | Type | Required | Description |
|---|---|---|---|
| `WIDTH` | Integer (1–50) | ✅ | Number of columns in the maze |
| `HEIGHT` | Integer (1–50) | ✅ | Number of rows in the maze |
| `ENTRY` | `row,col` | ✅ | Starting cell coordinates |
| `EXIT` | `row,col` | ✅ | Ending cell coordinates |
| `OUTPUT_FILE` | String | ✅ | Filename for the output file (written to `OUTPUT/`) |
| `PERFECT` | `true`/`false` | ✅ | If `true`, maze has no loops; if `false`, some walls are removed |
| `ALGORITHM` | `dfs` or `bt` | ❌ | Generation algorithm (default: `dfs`) |
| `SEED` | Integer | ❌ | Random seed for reproducible mazes |

**Constraints:**
- `WIDTH` and `HEIGHT` must each be between 1 and 50.
- `ENTRY` and `EXIT` must be within bounds and must not be the same cell.
- Neither `ENTRY` nor `EXIT` may overlap with the "42" pattern at the center.

### Output File Format

The output file is written to the `OUTPUT/` directory. Its format is:

```
<hex grid row 1>
<hex grid row 2>
...
<entry_row>,<entry_col>
<exit_row>,<exit_col>
<path string>
```

Each cell in the grid is encoded as a hexadecimal bitmask:
- Bit 0 (1) = North wall present
- Bit 1 (2) = East wall present
- Bit 2 (4) = South wall present
- Bit 3 (8) = West wall present

The path string uses `N`, `S`, `E`, `W` characters representing the sequence of directions from entry to exit.

---

## Maze Generation Algorithms

### DFS (Depth-First Search) — `ALGORITHM=dfs`

The DFS algorithm works by:
1. Starting from the entry cell and pushing it onto a stack.
2. Randomly choosing an unvisited neighbor and carving a passage to it.
3. Backtracking when no unvisited neighbors are available.
4. Repeating until all reachable cells have been visited.

**Why DFS?**
DFS was chosen as the primary algorithm because it produces mazes with long, winding corridors and relatively few dead ends near the start — making them visually impressive and genuinely challenging to navigate. It also maps naturally to a recursive/stack-based model and is straightforward to implement iteratively, which avoids Python's recursion limit for large grids. The resulting mazes have a strong visual texture and feel "hand-crafted."

---

### Binary Tree — `ALGORITHM=bt`

The Binary Tree algorithm processes each cell and carves a passage either **North** or **East** (chosen randomly). This creates a strong diagonal bias — all paths eventually flow toward the top-right corner — resulting in a simpler but less balanced maze. It is extremely fast and easy to implement.

---

### Imperfect Mazes (`PERFECT=false`)

When `PERFECT` is set to `false`, approximately 5% of the maze's walls are randomly removed after generation. This introduces cycles and loops, making the maze a **multigraph** rather than a spanning tree. The shortest path (solved via BFS) may then differ significantly from a simple DFS walk.

---

## Reusable Components

The following parts of the codebase are designed to be reusable:

### `MazeGenerator` class (`mazegen/generator.py`)
Fully self-contained. Accepts a configuration dict and exposes:
- `generate_maze()` → returns a maze dict with `grid`, `entry`, `exit`, `path`, and `pattern_42`
- `solve_maze()` → BFS solver, callable independently
- `dfs_algo()` / `binary_tree_algo()` → can be extended with additional algorithms by adding a new method and registering it in `generate_maze()`

To reuse it in another project:
```python
from mazegen.generator import MazeGenerator

config = {
    "WIDTH": 20, "HEIGHT": 20,
    "ENTRY": (0, 0), "EXIT": (19, 19),
    "PERFECT": True, "ALGORITHM": "dfs"
}
gen = MazeGenerator(config)
maze = gen.generate_maze()
```

### `display_maze()` (`mazegen/utils.py`)
Renders any maze dict to the terminal. Accepts wall emoji and path visibility as parameters — reusable for any grid-based maze structure that follows the same bitmask convention.

### `read_config()` / `validate_config()` (`mazegen/config.py`)
General-purpose key-value config parser with typed validation. Easily extensible to support new keys by adding parsing logic in `read_config()` and constraints in `validate_config()`.

---

## Team & Project Management

### Team Members & Roles

| Member | Role |
|---|---|
|  Oumaima NAANAA (onaanaa) | Maze generation algorithms (DFS, Binary Tree), 42 pattern embedding, BFS solver |
| Abdelghafour Akouryah (aakourya)  | Config parser, validation, terminal display, interactive UI, output file writing |

### Planning

**Initial Plan:**
- Week 1: Understand the project spec, design the grid data structure and bitmask representation, implement DFS.
- Week 2: Add BFS solver, config parser, and file output.
- Week 3: Terminal display with emoji rendering, interactive menu, imperfect maze support.
- Week 4: Testing, linting, README, polish.

**How It Evolved:**
- The 42 pattern embedding required more careful handling than anticipated — particularly ensuring the pattern cells are excluded from DFS traversal and that entry/exit validation accounts for them.
- The Binary Tree algorithm was added as a bonus once the core DFS pipeline was stable.
- The interactive display loop grew more complex with the addition of color themes and path toggling.

### What Worked Well
- The bitmask grid representation made wall manipulation and rendering clean and efficient.
- Separating config parsing, generation, and display into distinct modules kept the code maintainable.

### What Could Be Improved
- The `display_maze` function grew large; it could be split into a dedicated class.
- Add animation while showing the path.

### Tools Used
- **Python 3** — core language
- **flake8** — PEP8 linting
- **mypy** — static type checking
- **pdb** — debugging
- **Git** — version control and collaboration

---

## Advanced Features

### Multiple Algorithms
Two generation algorithms are supported and selectable via config: `dfs` (default) and `bt` (Binary Tree). Each produces structurally different mazes.

### Display Options
- **5 wall color themes** cycling through: ⬛ 🟫 🟥 🟩 🟪
- **Path overlay** toggle (shown in 🟦)
- **42 pattern** rendered in a contrasting color per theme
- **Entry** (🟢) and **Exit** (🔴) clearly marked

---

## Resources

### Maze Generation
- [BFS AND DFS Algorithms](https://www.youtube.com/watch?v=cS-198wtfj0)
- [BFS AND DFS Algorithms 2](https://www.youtube.com/watch?v=ioUl1M77hww)

### Pathfinding
- [BFS — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Visualgo — BFS/DFS Visualization](https://visualgo.net/en/bfs)


### Python
- [Python `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque)
- [Python `random` module](https://docs.python.org/3/library/random.html)

### AI Usage
AI (Claude by Anthropic) was used in the following ways during this project:
- **Debugging**: Identifying off-by-one errors in the bitmask wall-removal logic.
- **Code review**: Suggesting improvements to the config parser's error handling and type annotations.
- **Documentation**: Assisting in drafting this README, including structuring sections and describing algorithm tradeoffs.
- **No AI-generated code** was used for core algorithmic logic (DFS, BFS, Binary Tree) — these were implemented and understood by the team.