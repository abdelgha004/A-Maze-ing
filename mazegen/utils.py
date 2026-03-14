from typing import Any
import random
import time
from pathlib import Path


def write_maze(maze: dict, config: dict):
    output_dir = Path("OUTPUT")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / config["OUTPUT_FILE"]
    with open(output_path, 'w') as f:

        for row in maze["grid"]:
            line = "".join(format(cell, "X") for cell in row)
            f.write(line + '\n')

        f.write(f"\n{maze['entry'][0]},{maze['entry'][1]}\n")
        f.write(f"{maze['exit'][0]},{maze['exit'][1]}\n")

        f.write(f"{maze['path']}\n")

def display_maze(maze: dict[str, Any], wall: str = "⬛", show_path: bool = False) -> None:
    grid = maze["grid"]
    rows = len(grid)
    cols = len(grid[0])
    path = maze.get("path", "")

    entry = maze["entry"]
    exit = maze["exit"]

    height = 2 * rows + 1
    width = 2 * cols + 1

    WALL_TO_PATTERN = {
        "⬛": "🟧",  # black  → orange
        "🟥": "🟩",  # red    → yellow
        "🟩": "🟥",  # green  → purple
        "🟫": "🟪",  # yellow → red
        "🟪": "⬛",  # purple → orange
    }

    FLOOR = "⬜"
    ENTRY = "🟢"
    EXIT = "🔴"
    PATH = "🟦"
    PATTERN = WALL_TO_PATTERN.get(wall, "🟧")

    pattern_42 = maze.get("pattern_42", set())

    display = [[wall] * width for _ in range(height)]

    path_cells = set()
    if path and show_path:
        r, c = entry
        path_cells.add((r, c))
        for step in path:
            if step == 'N': r -= 1
            elif step == 'S': r += 1
            elif step == 'E': c += 1
            elif step == 'W': c -= 1
            path_cells.add((r, c))

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            vr = 2 * r + 1
            vc = 2 * c + 1

            # --- Cell center ---
            if (r, c) in pattern_42:
                display[vr][vc] = PATTERN
            elif (r, c) == entry:
                display[vr][vc] = ENTRY
            elif (r, c) == exit:
                display[vr][vc] = EXIT
            elif (r, c) in path_cells:
                display[vr][vc] = PATH
            else:
                display[vr][vc] = FLOOR

            # --- North wall slot ---
            if r > 0:
                if (r, c) in pattern_42 and (r - 1, c) in pattern_42:
                    display[vr - 1][vc] = PATTERN
                elif not (cell & 1) and (r - 1, c) not in pattern_42:
                    on_path = (r, c) in path_cells and (r - 1, c) in path_cells
                    display[vr - 1][vc] = PATH if on_path else FLOOR

            # --- South wall slot ---
            if r < rows - 1:
                if (r, c) in pattern_42 and (r + 1, c) in pattern_42:
                    display[vr + 1][vc] = PATTERN
                elif not (cell & 4) and (r + 1, c) not in pattern_42:
                    on_path = (r, c) in path_cells and (r + 1, c) in path_cells
                    display[vr + 1][vc] = PATH if on_path else FLOOR

            # --- West wall slot ---
            if c > 0:
                if (r, c) in pattern_42 and (r, c - 1) in pattern_42:
                    display[vr][vc - 1] = PATTERN
                elif not (cell & 8) and (r, c - 1) not in pattern_42:
                    on_path = (r, c) in path_cells and (r, c - 1) in path_cells
                    display[vr][vc - 1] = PATH if on_path else FLOOR

            # --- East wall slot ---
            if c < cols - 1:
                if (r, c) in pattern_42 and (r, c + 1) in pattern_42:
                    display[vr][vc + 1] = PATTERN
                elif not (cell & 2) and (r, c + 1) not in pattern_42:
                    on_path = (r, c) in path_cells and (r, c + 1) in path_cells
                    display[vr][vc + 1] = PATH if on_path else FLOOR

    for row in display:
        print("".join(row))


def run_interactive(maze, generator):
    wall_colors = ["⬛", "🟫", "🟥", "🟩", "🟪"]
    wall_index = 0
    path_visible = False

    display_maze(maze, wall=wall_colors[wall_index], show_path=path_visible)

    while True:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Change maze wall colours")
        print("4. Quit")

        choice = input("choice? (1-4): ").strip()

        if choice == "1":
            random.seed(time.time_ns())
            maze = generator.generate_maze()
            path_visible = False
            display_maze(maze, wall=wall_colors[wall_index], show_path=path_visible)
        elif choice == "2":
            path_visible = not path_visible
            display_maze(maze, wall=wall_colors[wall_index], show_path=path_visible)
        elif choice == "3":
            wall_index += 1
            if wall_index >= len(wall_colors):
                wall_index = 0
            display_maze(maze, wall=wall_colors[wall_index], show_path=path_visible)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")