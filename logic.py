from settings import *
from interface import Colors, Button, Menu, Action
import pygame as pg
import random

screen = pg.display.set_mode((WIDTH, HEIGHT))

class GameLogic:
    def __init__(self, cols, rows):
        self.grid = self.init_grid(cols, rows)
        self.generation = 0

     # Initialize the grid with random cells
    @staticmethod
    def init_grid(width, height):
        return {(x, y): 1 for y in range(height) for x in range(width) if random.choice([0, 1])}

    # Count the number of living neighbors for a given cell
    @staticmethod
    def count_neighbors(live_cells, x, y):
        return sum(((x + dx) % COLS, (y + dy) % ROWS) in live_cells for dx, dy in NEIGHBORS)

    # Update the grid based on the Game of Life rules
    @staticmethod
    def update_grid(live_cells, birth_rules=[3], survival_rules=[2, 3]):
        potential_cells = set(live_cells.keys()).union({((x + dx) % COLS, (y + dy) % ROWS) for x, y in live_cells for dx, dy in NEIGHBORS})
        neighbors_count = lambda cell: GameLogic.count_neighbors(live_cells.keys(), *cell)

        new_live_cells = {
            cell: (live_cells[cell] + 1 if cell in live_cells else 1)
            for cell in potential_cells
            if (cell in live_cells and neighbors_count(cell) in survival_rules) or neighbors_count(cell) in birth_rules
        }

        return new_live_cells

    @staticmethod
    def get_cell_color(age):
        if age == 1:
            return Colors.GREEN
        elif age < 5:
            return Colors.BROWN
        else:
            return Colors.BLACK

    def next_generation(self):
        self.grid = GameLogic.update_grid(self.grid)
        self.generation += 1

    @staticmethod
    def draw_grid(live_cells):
        screen.fill(Colors.WHITE)
        for (x, y), age in live_cells.items():
            color = GameLogic.get_cell_color(age)
            pg.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

class GameInterface:
    def __init__(self, game):
        self.game = game
        self.menu = self.create_menu()

    def create_menu(self):
        main_buttons = [
            Button(WIDTH // 2 - 50, 150, 100, 40, "Start", Action.START),
            Button(WIDTH // 2 - 50, 200, 100, 40, "Rules", Action.RULES),
            Button(WIDTH // 2 - 50, 250, 100, 40, "Reset", Action.RESET),
            Button(WIDTH // 2 - 50, 300, 100, 40, "Save", Action.SAVE),
            Button(WIDTH // 2 - 50, 350, 100, 40, "Load", Action.LOAD),
            Button(WIDTH // 2 - 50, 400, 100, 40, "Exit", Action.EXIT)
        ]
        return Menu(main_buttons)
