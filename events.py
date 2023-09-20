from settings import *
import pygame as pg

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
            self.game.notify_drag_start(cell)

        elif event.type == pg.MOUSEBUTTONUP and self.game.space_paused:
            self.game.notify_drag_end()

        elif event.type == pg.MOUSEMOTION and self.game.dragging and cell != self.game.last_modified_cell and self.game.space_paused:
            self.game.notify_drag_motion(cell)
