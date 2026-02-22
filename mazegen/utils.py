

def write_maze(maze, config):
    with open(config["OUTPUT_FILE"], 'w') as f:

        for row in maze["grid"]:
            line = "".join(format(cell, "X") for cell in row)
            f.write(line + '\n')

        f.write(f"\n{maze['entry'][0]},{maze['entry'][1]}\n")
        f.write(f"{maze['exit'][0]},{maze['exit'][1]}\n")

        f.write(f"{maze['path']}\n")


def display_maze(maze, wall: str = "⬛", show_path: bool = False) -> None:
    grid = maze["grid"]
    rows = len(grid)
    cols = len(grid[0])
    path = maze.get("path", "")

    entry = maze["entry"]
    exit = maze["exit"]

    height = 2 * rows + 1
    width = 2 * cols + 1

    FLOOR = "⬜"
    ENTRY = "🟢"
    EXIT  = "🔴"
    PATH  = "🟦"

    display = [[wall] * width for _ in range(height)]

    path_cells = set()

    if path and show_path:
        r, c = entry
        path_cells.add((r, c))
        for step in path:
            if step == 'N':
                r -= 1
            elif step == 'S':
                r += 1
            elif step == 'E':
                c += 1
            elif step == 'W':
                c -= 1
            path_cells.add((r, c))

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):

            vr = 2 * r + 1
            vc = 2 * c + 1

            if (r, c) == entry:
                display[vr][vc] = ENTRY
            elif (r, c) == exit:
                display[vr][vc] = EXIT
            elif (r, c) in path_cells:
                display[vr][vc] = PATH
            else:
                display[vr][vc] = FLOOR

            if not (cell & 1):
                on_path = (r, c) in path_cells and (r - 1, c) in path_cells
                display[vr - 1][vc] = PATH if on_path else FLOOR
            if not (cell & 4):
                on_path = (r, c) in path_cells and (r + 1, c) in path_cells
                display[vr + 1][vc] = PATH if on_path else FLOOR
            if not (cell & 8):
                on_path = (r, c) in path_cells and (r, c - 1) in path_cells
                display[vr][vc - 1] = PATH if on_path else FLOOR
            if not (cell & 2):
                on_path = (r, c) in path_cells and (r, c + 1) in path_cells
                display[vr][vc + 1] = PATH if on_path else FLOOR

    for row in display:
        print("".join(row))



def run_interactive(maze):
    wall_colors = ["⬛", "🟫", "🟥", "🟩", "🟧", "🟪"]
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
            # current_maze = generator.generate()   ← plug in later
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