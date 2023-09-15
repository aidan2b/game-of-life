#!/usr/bin/env python3

import random
import pygame as pg

# Constants for the display setting and colors
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 10
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
INITIAL_SPEED = 10
MIN_SPEED = 1
MAX_SPEED = 60

# Offets for checking neighboring cells in the grid
NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# Initialize the pygame library
pg.init()
pg.font.init()

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
def handle_event(event, grid, fps):
    global dragging, last_modified_cell

    if event.type == pg.QUIT:
        return False, fps

    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
        return 'toggle_pause', fps

    if event.type == pg.KEYDOWN and event.key == pg.K_UP and fps < MAX_SPEED:
        fps += 1

    if event.type == pg.KEYDOWN and event.key == pg.K_DOWN and fps > MIN_SPEED:
        fps -= 1

    x, y = pg.mouse.get_pos()
    cell = (x // CELL_SIZE, y // CELL_SIZE)

    if event.type == pg.MOUSEBUTTONDOWN:
        dragging = True
        grid ^= {cell}
        last_modified_cell = cell
    elif event.type == pg.MOUSEBUTTONUP:
        dragging, last_modified_cell = False, None
        return True, fps
    elif event.type == pg.MOUSEMOTION and dragging and cell != last_modified_cell:
        grid ^= {cell}
        last_modified_cell = cell

    return True, fps

# Draw statistics on the screen
# Additional colors and font initialization

BORDER_COLOR = (255, 255, 255)
font_small = pg.font.Font(None, 36)

def display_statistics(grid, generation, fps, clock):
    # Get the number of live cells
    num_live_cells = len(grid)

    # Render text for stats
    live_cells_text = font_small.render(f'Live Cells: {num_live_cells}', True, BLACK)
    generation_text = font_small.render(f'Generation: {generation}', True, BLACK)
    fps_text = font_small.render(f'FPS: {int(clock.get_fps())}', True, GREEN)

    # Create a white background surface for stats and draw a border around it
    stats_bg = pg.Surface((WIDTH//3, 75))
    stats_bg.fill(WHITE)
    pg.draw.rect(stats_bg, BORDER_COLOR, stats_bg.get_rect(), 3)  # 3 pixels border width

    # Blit the statistics text onto the stats background surface
    stats_bg.blit(live_cells_text, (10, 5))
    stats_bg.blit(generation_text, (10, 40))

    # Draw the stats background surface and FPS text onto the main screen
    screen.blit(stats_bg, (10, HEIGHT - 85))
    screen.blit(fps_text, (WIDTH - 100, 10))

# Run the simulation
def main():
    grid = init_grid(COLS, ROWS)
    clock = pg.time.Clock()
    running = True
    paused = False
    generation = 0
    fps = INITIAL_SPEED

    # Create a font object for statistics display
    font = pg.font.SysFont(None, 24)

    while running:
        screen.fill(WHITE)

        for event in pg.event.get():
            result, new_fps = handle_event(event, grid, fps)
            if result == False:
                running = False
            if result == 'toggle_pause':
                paused = not paused
            fps = new_fps

        if not paused:
            grid = update_grid(grid)
            generation += 1

        draw_grid(grid)
        display_statistics(grid, generation, 10, clock)
        pg.display.flip()
        clock.tick(fps)

    pg.quit()

if __name__ == '__main__':
    main()
