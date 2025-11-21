import numpy as np
import random

def generate_maze(rows=21, cols=21):
    # Ensure odd size (required for maze generation)
    if rows % 2 == 0: rows += 1
    if cols % 2 == 0: cols += 1

    maze = np.ones((rows, cols), dtype=np.int8)

    # Start cell
    stack = [(1, 1)]
    maze[1, 1] = 0

    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    while stack:
        r, c = stack[-1]

        neighbours = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows - 1 and 1 <= nc < cols - 1:
                if maze[nr, nc] == 1:
                    neighbours.append((nr, nc))

        if not neighbours:
            stack.pop()
            continue

        nr, nc = random.choice(neighbours)

        maze[r + (nr - r) // 2, c + (nc - c) // 2] = 0
        maze[nr, nc] = 0
        stack.append((nr, nc))

    return maze
