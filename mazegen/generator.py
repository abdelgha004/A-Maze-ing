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

    def __init__(self, config):
        """ Constructor """
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.rndom_g = random.Random(config.get('seed', None))
        self.grid = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]
        self.patt_42 = self.create_42()
        if self.entry in self.patt_42:
            raise ValueError(f"Entry {self.entry} is inside the 42 pattern!")
        if self.exit in self.patt_42:
            raise ValueError(f"Exit {self.exit} is inside the 42 pattern!")

    def create_42(self):
        """ Creates 42 pattern in center of Maze"""
        pass
    def generate_maze(self):
        """ Backtracking DFS generator """
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
        return {
            'grid': self.grid,
            'entry': self.entry,
            'exit': self.exit,
            'path': self.solve_maze()
        }

    def solve_maze(self):
        """ Find shortest path using BFS"""
        queue = deque()
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