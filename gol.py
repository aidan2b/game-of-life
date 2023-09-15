#!/usr/bin/env python3

import random

WIDTH, HEIGHT = 10,10

# Initializes the game board
def init_grid(width, height):

    return [[random.choice([0, 1]) for x in range(width)] for y in range(height)]

# Counts the number of living neighbors for a given cell
def count_neighbors(grid, x, y):

    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    count = 0

    # Loop through each neighbor offset and check if the neighbor is within the grid boundaries and alive
    for dx, dy in neighbors:
        nx, ny = x + dx, y + dy
        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
            count += grid[ny][nx]
    return count

# Apply the rules of Conway's Game of Life
def update_grid(grid):

    new_grid = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]

    for y in range(HEIGHT):
        for x in range(WIDTH):

            neighbors = count_neighbors(grid, x, y)

            # A living cell with < 2 or > 3 living neighbors will die
            if grid[y][x] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[y][x] = 0

            # A dead cell with exactly 3 living neighbors becomes alive
            elif grid[y][x] == 0 and neighbors == 3:
                new_grid[y][x] = 1

            # All other cells retain their current state
            else:
                new_grid[y][x] = grid[y][x]
    return new_grid

# Displays the current state of the grid in the console
def print_grid(grid):
    for row in grid:
        print(''.join(['#' if cell else '.' for cell in row]))

grid = init_grid(WIDTH, HEIGHT)

for i in range(10):
    print_grid(grid)
    print("\n-----\n")
    grid = update_grid(grid)
