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

    live_cells = set()

    for y in range(height):
        for x in range(width):
            if random.choice([0,1]):
                live_cells.add((x,y))

    return live_cells
    
# Counts the number of living neighbors for a given cell
def count_neighbors(live_cells, x, y):

    neighbors_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    count = 0

    # Loop through each neighbor offset and check if the neighbor is within the grid boundaries and alive
    for dx, dy in neighbors_offsets:
        if (x + dx, y + dy) in live_cells:
            count += 1
    return count

# Apply the rules of Conway's Game of Life
def update_grid(live_cells):

    new_live_cells = set()

    neighbors_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    potential_cells = live_cells.union({(x+dx, y+dy) for x,y in live_cells
                                           for dx, dy in neighbors_offsets})

    for cell in potential_cells:
        x, y = cell
        count = count_neighbors(live_cells, x, y)
        if cell in live_cells and (count == 2 or count == 3):
            new_live_cells.add(cell)
        elif cell not in live_cells and count == 3:
            new_live_cells.add(cell)

    return new_live_cells

# Drawing the grid
def draw_grid(live_cells, screen, changed_cells=None):
    if changed_cells is None:
        screen.fill(WHITE)
        for cell in live_cells:
            x, y = cell
            pg.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    else:
        for cell in changed_cells:
            x, y = cell
            color = BLACK if cell in live_cells else WHITE
            pg.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

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
                cell = (x, y)

                if cell in grid:
                    grid.remove(cell)
                else:
                    grid.add(cell)

        if not paused:
            grid = update_grid(grid)

        draw_grid(grid, screen)
        pg.display.flip()
        clock.tick(10)

    pg.quit()

if __name__ == '__main__':
    main()
