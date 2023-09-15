#!/usr/bin/env python3

import random
import pygame as pg

# Constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 10
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pg.init()

# Initialization
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Conway's Game of Life")

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
        if 0 <= nx < COLS and 0 <= ny < ROWS:
            count += grid[ny][nx]
    return count

# Apply the rules of Conway's Game of Life
def update_grid(grid):

    new_grid = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]

    for y in range(ROWS):
        for x in range(COLS):

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

# Drawing the grid
def draw_grid(grid, screen):
    for y in range(ROWS):
        for x in range(COLS):
            color = BLACK if grid[y][x] else WHITE
            pg.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pg.draw.line(screen, (200, 200, 200), (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
            pg.draw.line(screen, (200, 200, 200), (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))

def main():
    grid = init_grid(COLS, ROWS)
    clock = pg.time.Clock()
    running = True
    paused = False

    while running:
        screen.fill(WHITE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    paused = not paused
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                x //= CELL_SIZE
                y //= CELL_SIZE
                grid[y][x] = 1 if grid[y][x] == 0 else 0 # Toggle cell state

        if not paused:
            grid = update_grid(grid)

        draw_grid(grid, screen)
        pg.display.flip()
        clock.tick(10)

    pg.quit()

if __name__ == '__main__':
    main()
