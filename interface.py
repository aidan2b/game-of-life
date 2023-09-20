from settings import *
import pygame as pg
from enum import Enum, auto

pg.font.init()
font = pg.font.Font(None, 32)
font_small = pg.font.Font(None, 28)
screen = pg.display.set_mode((WIDTH, HEIGHT))

class Action(Enum):

    START = auto()
    RULES = auto()
    RESET = auto()
    EXIT = auto()
    SAVE = auto()
    LOAD = auto()

class Colors:

    BLACK = (32, 38, 46)
    GREEN = (205, 88, 136)
    WHITE = (233, 232, 232)
    BROWN = (145, 49, 117)

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

class Statistics:

    def __init__(self, grid, generation, fps, clock):
        self.grid = grid
        self.generation = generation
        self.fps = fps
        self.clock = clock

    def display_statistics(self, screen):
        # Get the number of live cells
        num_live_cells = len(self.grid)

        # Render text for stats
        live_cells_text = font.render(f'Live Cells: {num_live_cells}', True, Colors.BLACK)
        generation_text = font.render(f'Generation: {self.generation}', True, Colors.BLACK)

        # Create a white background surface for stats and draw a border around it
        stats_bg = pg.Surface((BOX_WIDTH, BOX_HEIGHT))
        stats_bg.fill(Colors.WHITE)
        pg.draw.rect(stats_bg, Colors.BLACK, stats_bg.get_rect(), 3)  # 3 pixels border width

        # Blit the statistics text onto the stats background surface
        stats_bg.blit(live_cells_text, (PADDING, 5))
        stats_bg.blit(generation_text, (PADDING, 40))

        # Draw the stats background surface onto the main screen
        screen.blit(stats_bg, (10, HEIGHT - BOX_HEIGHT - PADDING))

class Slider:

    def __init__(self, x, y, width, min_val, max_val, initial_val):
        self.x = WIDTH - BOX_WIDTH - PADDING  # Adjust the x-position for right side with padding.
        self.y = y
        self.width = width
        self.min = min_val
        self.max = max_val
        self.value = initial_val
        self.dragging = False
        self.circle_radius = 10
        self.line_height = 5
        self.SLIDER_LINE_PADDING = (BOX_WIDTH - self.width) // 2

    def get_value(self):
        return self.value

    def draw(self, screen):
        box = pg.Surface((BOX_WIDTH, BOX_HEIGHT))
        box.fill(Colors.WHITE)
        pg.draw.rect(box, Colors.BLACK, box.get_rect(), 3)  # 3 pixels border width

        # Slider line
        pg.draw.line(box, Colors.BLACK,
             (self.SLIDER_LINE_PADDING, BOX_HEIGHT // 2),
             (BOX_WIDTH - self.SLIDER_LINE_PADDING, BOX_HEIGHT // 2),
             self.line_height)

        # Slider circle
        circle_x = self.SLIDER_LINE_PADDING + (self.value - self.min) / (self.max - self.min) * self.width
        pg.draw.circle(box, Colors.GREEN, (int(circle_x), BOX_HEIGHT // 2), self.circle_radius)

        # Display FPS above the slider
        fps_text = font_small.render(f'FPS: {int(self.value)}', True, Colors.BLACK)
        text_rect = fps_text.get_rect(center=(BOX_WIDTH // 2, 15))  # 15 is a position above the slider
        box.blit(fps_text, text_rect)

        screen.blit(box, (self.x, HEIGHT - BOX_HEIGHT - PADDING))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mx, my = event.pos
            circle_x = self.x + self.SLIDER_LINE_PADDING + (self.value - self.min) / (self.max - self.min) * self.width
            circle_y = HEIGHT - BOX_HEIGHT - PADDING + BOX_HEIGHT // 2
            if (mx - circle_x)**2 + (my - circle_y)**2 < self.circle_radius**2:
                self.dragging = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pg.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            self.value = (mx - self.x - PADDING) / self.width * (self.max - self.min) + self.min
            self.value = min(self.max, max(self.min, self.value))

