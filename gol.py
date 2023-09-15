#!/usr/bin/env python3

import random
import pygame as pg

# Constants for the display setting and colors
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 10
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Offets for checking neighboring cells in the grid
NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# Initialize the pygame library
pg.init()

# Set up the display window for the simulation
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Conway's Game of Life")

# Initialize the grid with random cells
def init_grid(width, height):
    return {(x, y) for y in range(height) for x in range(width) if random.choice([0, 1])}

# Count the number of living neighbors for a given cell
def count_neighbors(live_cells, x, y):
    return sum((x + dx, y + dy) in live_cells for dx, dy in NEIGHBORS)

# Update the grid based on the Game of Life rules
def update_grid(live_cells):
    potential_cells = live_cells.union({(x + dx, y + dy) for x, y in live_cells for dx, dy in NEIGHBORS})
    is_alive = lambda cell: (cell in live_cells and 2 <= count_neighbors(live_cells, *cell) <= 3) or count_neighbors(live_cells, *cell) == 3
    return {cell for cell in potential_cells if is_alive(cell)}

# Draw the live cells on the grid
def draw_grid(live_cells):
    screen.fill(WHITE)

    for x, y in live_cells:
        pg.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Variables to track dragging and the last modified cell during a drag
dragging, last_modified_cell = False, None

# Handle user inputs/events like quit, pause, or adding/removing cells
def handle_event(event, grid):
    global dragging, last_modified_cell

    if event.type == pg.QUIT:
        return False

    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
        return 'toggle_pause'

    x, y = pg.mouse.get_pos()
    cell = (x // CELL_SIZE, y // CELL_SIZE)

    if event.type == pg.MOUSEBUTTONDOWN:
        dragging = True
        grid ^= {cell}
        last_modified_cell = cell
    elif event.type == pg.MOUSEBUTTONUP:
        dragging, last_modified_cell = False, None
        return True
    elif event.type == pg.MOUSEMOTION and dragging and cell != last_modified_cell:
        grid ^= {cell}
        last_modified_cell = cell
    return True

# Run the simulation
def main():
    grid = init_grid(COLS, ROWS)
    clock = pg.time.Clock()
    running = True
    paused = False

    while running:
        screen.fill(WHITE)

        for event in pg.event.get():
            result = handle_event(event, grid)
            if result == False:
                running = False
            if result == 'toggle_pause':
                paused = not paused

        if not paused:
            grid = update_grid(grid)

        draw_grid(grid)
        pg.display.flip()
        clock.tick(10)

    pg.quit()

if __name__ == '__main__':
    main()
