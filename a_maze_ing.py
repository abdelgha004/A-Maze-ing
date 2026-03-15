import sys
from config import read_config, validate_config
from utils import write_maze, run_interactive
from mazegen.generator import MazeGenerator


def main() -> None:
    try:
        if len(sys.argv) != 2:
            print("Usage: python a_maze_ing.py <maze_file>")
            sys.exit(1)

        config_file = sys.argv[1]

        config = read_config(config_file)
        try:
            validate_config(config)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        try:
            generator = MazeGenerator(config)
            maze = generator.generate_maze()
            write_maze(maze, config)
            run_interactive(maze, generator)
        except ValueError as e:
            print(e)
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)


if __name__ == "__main__":
    main()
