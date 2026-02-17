import sys
from mazegen.config import read_config, validate_config
# from mazegen.maze import Maze

def main():
	
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
	print("Configuration is valid. Ready to generate maze.")
	print(config)


if __name__ == "__main__":
	main()