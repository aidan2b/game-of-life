#!/usr/bin/env python3

from settings import *
from ui import Colors, Button, Menu, Slider, Action
from core import GameLogic, GameInterface, EventHandler
import pygame as pg
from tkinter import filedialog, Tk
import pickle

pg.init()
pg.font.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Conway's Game of Life")
font = pg.font.Font(None, 32)
font_small = pg.font.Font(None, 28)

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

    pass

if __name__ == '__main__':
    game = Game()
    game.run()
    pass
