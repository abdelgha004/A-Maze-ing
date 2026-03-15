import random
from collections import deque


class MazeGenerator:
    """ Maze generator class definition"""
    N = 1
    E = 2
    S = 4
    W = 8

    directions = {
        N: (-1, 0),
        E: (0, 1),
        S: (1, 0),
        W: (0, -1)
    }

    opp_direction = {
        N: S,
        E: W,
        S: N,
        W: E
    }

    path_char = {
        N: 'N',
        E: 'E',
        S: 'S',
        W: 'W'
    }

    def __init__(self, config: dict):
        """ Constructor """
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.perfect = config["PERFECT"]
        self.algo = config.get("ALGORITHM", "dfs")
        self.rndom_g = random.Random(config.get('SEED', None))
        self.grid = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]
        self.patt_42 = self.create_42()
        if self.entry in self.patt_42:
            raise ValueError(f"Entry {self.entry} is inside the 42 pattern!")
        if self.exit in self.patt_42:
            raise ValueError(f"Exit {self.exit} is inside the 42 pattern!")

    def create_42(self) -> set:
        """ Creates 42 pattern in center of Maze"""

        center_r = self.height // 2
        center_c = self.width // 2

        four = [
            "X X",
            "X X",
            "XXX",
            "  X",
            "  X"
        ]

        two = [
            "XXX",
            "  X",
            "XXX",
            "X  ",
            "XXX"
        ]

        digit_h = len(four)
        digit_w = len(four[0])

        # digit height + vertical padding
        min_height = 5 + 2
        # four_w + gap + two_w + horizontal padding
        min_width = len(four[0]) + 1 + len(two[0]) + 4

        if self.height < min_height or self.width < min_width:
            print(f"Warning: maze is too small ({self.width}x{self.height}) to"
                  f" display the '42' pattern. It will be omitted.\n"
                  f"Min height = {min_height}\nMin width = {min_width}")
            return set()
        pattern = set()

        top = center_r - digit_h // 2
        left_four = center_c - digit_w - 1
        left_two = center_c + 1

        # 4
        for r in range(digit_h):
            for c in range(digit_w):
                if four[r][c] == "X":
                    pattern.add((top + r, left_four + c))

        # 2
        for r in range(digit_h):
            for c in range(digit_w):
                if two[r][c] == "X":
                    pattern.add((top + r, left_two + c))
        return pattern

    def make_maze_not_perfect(self) -> None:
        """ Making the Maze not perfect """
        num_cells = round((self.height * self.width) * 0.05)
        opened = 0

        dirs = list(self.directions.items())

        while opened < num_cells:

            r = self.rndom_g.randrange(self.height)
            c = self.rndom_g.randrange(self.width)

            if (r, c) in self.patt_42:
                continue

            direction, (dr, dc) = self.rndom_g.choice(dirs)

            nr = r + dr
            nc = c + dc

            if not (0 <= nr < self.height and 0 <= nc < self.width):
                continue

            if (nr, nc) in self.patt_42:
                continue

            # only break walls that still exist
            if self.grid[r][c] & direction:
                self.grid[r][c] &= ~direction
                self.grid[nr][nc] &= ~self.opp_direction[direction]
                opened += 1

    def dfs_algo(self) -> dict:
        """ Generate maze using DFS algo """
        self.grid = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]
        visited = [
            [False]*self.width for _ in range(self.height)
        ]
        stack = []
        r, c = self.entry
        visited[r][c] = True
        stack.append((r, c))
        while stack:
            r, c = stack[-1]
            neighbors = []
            for direction, (dr, dc) in self.directions.items():
                nr = r + dr
                nc = c + dc
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    if not visited[nr][nc] and (nr, nc) not in self.patt_42:
                        neighbors.append((direction, nr, nc))
            if neighbors:
                direction, nr, nc = self.rndom_g.choice(neighbors)
                self.grid[r][c] &= ~direction
                self.grid[nr][nc] &= ~self.opp_direction[direction]
                visited[nr][nc] = True
                stack.append((nr, nc))
            else:
                stack.pop()
        if not self.perfect:
            self.make_maze_not_perfect()
        return {
                "grid": self.grid,
                "entry": self.entry,
                "exit": self.exit,
                "path": self.solve_maze(),
                "pattern_42": self.patt_42,
            }

    def binary_tree_algo(self) -> dict:
        """ Generate maze using binary tree algorithm """
        self.grid = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]

        for r in range(self.height):
            for c in range(self.width):

                if (r, c) in self.patt_42:
                    continue

                neighbors = []

                # north
                if r > 0 and (r - 1, c) not in self.patt_42:
                    neighbors.append((self.N, -1, 0))

                # east
                if c < self.width - 1 and (r, c + 1) not in self.patt_42:
                    neighbors.append((self.E, 0, 1))

                if neighbors:
                    direction, dr, dc = self.rndom_g.choice(neighbors)

                    nr = r + dr
                    nc = c + dc

                    self.grid[r][c] &= ~direction
                    self.grid[nr][nc] &= ~self.opp_direction[direction]
        if not self.perfect:
            self.make_maze_not_perfect()
        return {
                "grid": self.grid,
                "entry": self.entry,
                "exit": self.exit,
                "path": self.solve_maze(),
                "pattern_42": self.patt_42,
            }

    def generate_maze(self,) -> dict:
        """ Backtracking DFS generator """
        if self.algo == "dfs":
            return self.dfs_algo()
        elif self.algo == "bt":
            return self.binary_tree_algo()
        return {}

    def solve_maze(self) -> str:
        """ Find shortest path using BFS"""
        queue: deque = deque()
        visited = [[False] * self.width for _ in range(self.height)]
        parent = {}

        queue.append(self.entry)
        visited[self.entry[0]][self.entry[1]] = True

        while queue:
            r, c = queue.popleft()
            if (r, c) == self.exit:
                break
            for direction, (dr, dc) in self.directions.items():
                if self.grid[r][c] & direction:
                    continue
                nr = r + dr
                nc = c + dc
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    if not visited[nr][nc]:
                        visited[nr][nc] = True
                        parent[(nr, nc)] = ((r, c), direction)
                        queue.append((nr, nc))

        path = []
        cell = self.exit
        while cell != self.entry:
            prev, direction = parent[cell]
            path.append(direction)
            cell = prev
        path.reverse()
        path_str = "".join(self.path_char[d] for d in path)
        return path_str
