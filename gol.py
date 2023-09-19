#!/usr/bin/env python3

import random
from enum import Enum, auto
import pygame as pg
from tkinter import filedialog, Tk
import pickle
import os

# Constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 10
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
INITIAL_SPEED, MIN_SPEED, MAX_SPEED = 10, 1, 60
NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# Colors
class Colors:
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    BROWN = (111, 78, 55)

# Actions for Menu Buttons
class Action(Enum):
    START = auto()
    RULES = auto()
    RESET = auto()
    EXIT = auto()
    SAVE = auto()
    LOAD = auto()

pg.init()
pg.font.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Conway's Game of Life")
font = pg.font.Font(None, 36)
font_small = pg.font.Font(None, 24)

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, screen):
        pg.draw.rect(screen, Colors.BLACK, self.rect, 2)
        label = font.render(self.text, True, Colors.BLACK)
        text_width, text_height = label.get_size()

        # Calculate positions to center the text
        centered_x = self.rect.x + (self.rect.width - text_width) // 2
        centered_y = self.rect.y + (self.rect.height - text_height) // 2

        screen.blit(label, (centered_x, centered_y))

    def is_clicked(self, x, y):
        if self.rect.collidepoint(x, y):
            return self.action

class Menu:
    def __init__(self, buttons):
        self.buttons = buttons

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            for button in self.buttons:
                if button.is_clicked(x, y):
                    return button.action
        return None

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val):
        self.x = x
        self.y = y
        self.width = width
        self.min = min_val
        self.max = max_val
        self.value = initial_val
        self.dragging = False
        self.circle_radius = 10
        self.line_height = 5

    def draw(self, screen):
        box_width = self.width + 20  # A little padding
        box_height = 60  # Adjust as needed
        box = pg.Surface((box_width, box_height))
        box.fill(Colors.WHITE)
        pg.draw.rect(box, Colors.BLACK, box.get_rect(), 3)  # 3 pixels border width

        # Slider line
        pg.draw.line(box, Colors.BLACK, (10, box_height // 2), (self.width + 10, box_height // 2), self.line_height)

        # Slider circle
        circle_x = 5 + (self.value - self.min) / (self.max - self.min) * self.width
        pg.draw.circle(box, Colors.GREEN, (int(circle_x), box_height // 2), self.circle_radius)

        # Display FPS above the slider
        fps_text = font_small.render(f'FPS: {int(self.value)}', True, Colors.BLACK)
        text_rect = fps_text.get_rect(center=(box_width // 2, 15))  # 15 is a position above the slider
        box.blit(fps_text, text_rect)

        screen.blit(box, (self.x - 10, self.y - (box_height // 2)))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mx, my = event.pos
            circle_x = self.x + (self.value - self.min) / (self.max - self.min) * self.width
            if (mx - circle_x)**2 + (my - self.y)**2 < self.circle_radius**2:
                self.dragging = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pg.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            self.value = (mx - self.x) / self.width * (self.max - self.min) + self.min
            self.value = min(self.max, max(self.min, self.value))

    def get_value(self):
        return int(self.value)

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

    def draw_grid(self, live_cells):
        screen.fill(Colors.WHITE)
        for (x, y), age in live_cells.items():
            color = GameLogic.get_cell_color(age)
            pg.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def display_statistics(self, grid, generation, fps, clock):
        # Get the number of live cells
        num_live_cells = len(grid)

        # Render text for stats
        live_cells_text = font.render(f'Live Cells: {num_live_cells}', True, Colors.BLACK)
        generation_text = font.render(f'Generation: {generation}', True, Colors.BLACK)

        # Create a white background surface for stats and draw a border around it
        stats_bg = pg.Surface((WIDTH//3, 75))
        stats_bg.fill(Colors.WHITE)
        pg.draw.rect(stats_bg, Colors.BLACK, stats_bg.get_rect(), 3)  # 3 pixels border width

        # Blit the statistics text onto the stats background surface
        stats_bg.blit(live_cells_text, (10, 5))
        stats_bg.blit(generation_text, (10, 40))

        # Draw the stats background surface and FPS text onto the main screen
        screen.blit(stats_bg, (10, HEIGHT - 85))

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
    def update_grid(live_cells):
        potential_cells = set(live_cells.keys()).union({((x + dx) % COLS, (y + dy) % ROWS) for x, y in live_cells for dx, dy in NEIGHBORS})
        is_alive = lambda cell: (cell in live_cells and 2 <= GameLogic.count_neighbors(live_cells.keys(), *cell) <= 3) or GameLogic.count_neighbors(live_cells.keys(), *cell) == 3
        new_live_cells = {cell: (live_cells[cell] + 1 if cell in live_cells else 1) for cell in potential_cells if is_alive(cell)}
        return new_live_cells

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

class EventHandler:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):

        x, y = pg.mouse.get_pos()
        cell = (x // CELL_SIZE, y // CELL_SIZE)

        if event.type == pg.QUIT:
            self.game.running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.game.space_paused = not self.game.space_paused
            elif event.key == pg.K_UP and self.game.fps < MAX_SPEED:
                self.game.fps += 1
            elif event.key == pg.K_DOWN and self.game.fps > MIN_SPEED:
                self.game.fps -= 1
            elif event.key == pg.K_ESCAPE:
                self.game.menu_active = True
                self.game.paused = True

        elif event.type == pg.MOUSEBUTTONDOWN and self.game.space_paused:
            self.game.dragging = True
            if cell in self.game.grid:
                del self.game.grid[cell]
            else:
                self.game.grid[cell] = 1

            self.game.last_modified_cell = cell

        elif event.type == pg.MOUSEBUTTONUP and self.game.space_paused:
            self.game.dragging, self.game.last_modified_cell = False, None

        elif event.type == pg.MOUSEMOTION and self.game.dragging and cell != self.game.last_modified_cell and self.game.space_paused:
            if cell in self.game.grid:
                del self.game.grid[cell]
            else:
                self.game.grid[cell] = 1
            self.game.last_modified_cell = cell

class Game:
    def __init__(self):
        self.interface = GameInterface(self)
        self.handler = EventHandler(self)
        self.grid = GameLogic.init_grid(COLS, ROWS)
        self.clock = pg.time.Clock()
        self.running = True
        self.paused = False
        self.generation = 0
        self.fps = INITIAL_SPEED
        self.fps_slider = Slider(WIDTH - 210, HEIGHT - 50, 200, MIN_SPEED, MAX_SPEED, INITIAL_SPEED)
        self.menu_active = True
        self.space_paused = False
        self.dragging, self.last_modified_cell = False, None

    def save(self):
        # Use tkinter to show a save file dialog
        root = Tk()
        root.withdraw()  # Hide the tkinter main window
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'wb') as file:
                pickle.dump(self.grid, file)
        root.destroy()

    def load(self):
        # Use tkinter to show an open file dialog
        root = Tk()
        root.withdraw()  # Hide the tkinter main window
        file_path = filedialog.askopenfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    self.grid = pickle.load(file)
            except (EOFError, pickle.UnpicklingError):
                print("Error: Failed to load the game state.")
        root.destroy()

    def execute_action(self, action):
        if action == Action.START:
            self.menu_active = False
            self.paused = False
        elif action == Action.RULES:
            # TODO: implement rules display or logic
            pass
        elif action == Action.RESET:
            self.grid = GameLogic.init_grid(COLS, ROWS)
            self.generation = 0
            self.menu_active = False
            self.paused = False
        elif action == Action.SAVE:
            self.save()
        elif action == Action.LOAD:
            self.load()
        elif action == Action.EXIT:
            self.running = False

    # Run the simulation
    def run(self):
        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((255, 255, 255))

        while self.running:
            screen.fill(Colors.WHITE)

            for event in pg.event.get():
                if self.menu_active:
                    if event.type == pg.QUIT:
                        self.running = False
                        break

                    action = self.interface.menu.handle_event(event)
                    if action:
                        self.execute_action(action)

                elif not self.menu_active:
                    self.handler.handle_event(event)
                    self.fps_slider.handle_event(event)

            if not self.paused and not self.menu_active and not self.space_paused:
                self.grid = GameLogic.update_grid(self.grid)
                self.generation += 1

            self.interface.draw_grid(self.grid)

            self.interface.display_statistics(self.grid, self.generation, 10, self.clock)

            self.fps_slider.draw(screen)
            self.fps = self.fps_slider.get_value()

            if self.menu_active:
                screen.blit(overlay, (0, 0))
                self.interface.menu.draw(screen)

            pg.display.flip()
            self.clock.tick(self.fps)

        pg.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
