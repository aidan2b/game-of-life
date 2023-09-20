import pickle
from tkinter import filedialog, Tk
import pygame as pg

from settings import *
from interface import Action, Colors, Button, Menu, Statistics, Slider
from logic import GameLogic, GameInterface
from events import EventHandler

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Conway's Game of Life")

        self.interface = GameInterface(self)
        self.handler = EventHandler(self)
        self.grid = self.initialize_grid()
        self.clock = pg.time.Clock()
        self.setup_game_variables()

    def initialize_grid(self):
        return GameLogic.init_grid(COLS, ROWS)

    def setup_game_variables(self):
        self.running = True
        self.paused = False
        self.generation = 0
        self.fps = INITIAL_SPEED
        self.fps_slider = Slider(WIDTH - 210, HEIGHT - 50, 200, MIN_SPEED, MAX_SPEED, INITIAL_SPEED)
        self.statistics = Statistics(self.grid, self.generation, self.fps, self.clock)
        self.menu_active = True
        self.space_paused = False
        self.dragging, self.last_modified_cell = False, None
        self.birth_rules = [3]
        self.survival_rules = [2, 3]

    def show_save_dialog(self):
        root = Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")])
        root.destroy()
        return file_path

    def show_load_dialog(self):
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")])
        root.destroy()
        return file_path

    def save(self):
        file_path = self.show_save_dialog()
        if file_path:
            with open(file_path, 'wb') as file:
                pickle.dump(self.grid, file)

    def load(self):
        file_path = self.show_load_dialog()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    self.grid = pickle.load(file)
            except (EOFError, pickle.UnpicklingError):
                print("Error: Failed to load the game state.")

    def parse_rules(self, rule_string):
        birth, survival = rule_string.split('/')
        birth = [int(b) for b in birth[1:]]
        survival = [int(s) for s in survival[1:]]
        return birth, survival

    def execute_action(self, action):
        if action == Action.START:
            self.menu_active = False
            self.paused = False
        elif action == Action.RULES:
            rule_string = input("Enter the rule string (e.g., B3/S23 for the standard Game of Life): ")
            try:
                self.birth_rules, self.survival_rules = self.parse_rules(rule_string)
                print("Rules updated successfully!")
            except ValueError:
                print("Invalid rule string format!")

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

    def notify_drag_start(self, cell):
        self.dragging = True
        if cell in self.grid:
            del self.grid[cell]
        else:
            self.grid[cell] = 1
        self.last_modified_cell = cell

    def notify_drag_end(self):
        self.dragging, self.last_modified_cell = False, None

    def notify_drag_motion(self, cell):
        if cell in self.grid:
            del self.grid[cell]
        else:
            self.grid[cell] = 1
        self.last_modified_cell = cell

    def run(self):
        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((255, 255, 255))

        while self.running:
            self.process_events(overlay)
            pg.display.flip()
            self.clock.tick(self.fps)

        pg.quit()

    def process_events(self, overlay):
        self.screen.fill(Colors.WHITE)

        for event in pg.event.get():
            self.handle_main_events(event)

            if not self.menu_active:
                self.handler.handle_event(event)
                self.fps_slider.handle_event(event)

        self.update_simulation()
        self.draw_elements(overlay)

    def handle_main_events(self, event):
        if event.type == pg.QUIT:
            self.running = False
            return

        if self.menu_active:
            action = self.interface.menu.handle_event(event)
            if action:
                self.execute_action(action)

    def update_simulation(self):
        if not self.paused and not self.menu_active and not self.space_paused:
            self.grid = GameLogic.update_grid(self.grid, self.birth_rules, self.survival_rules)
            self.generation += 1
            self.statistics.grid = self.grid
            self.statistics.generation = self.generation

    def draw_elements(self, overlay):
        GameLogic.draw_grid(self.grid)
        self.statistics.display_statistics(self.screen)
        self.fps_slider.draw(self.screen)
        self.fps = self.fps_slider.get_value()
        if self.menu_active:
            self.screen.blit(overlay, (0, 0))
            self.interface.menu.draw(self.screen)

if __name__ == '__main__':
    game = Game()
    game.run()
