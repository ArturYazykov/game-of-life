import random
from enum import Enum

import pygame
from pygame.locals import *

from cell import Cell
from info import GameInfo
from utils import _time


class MouseBTnState(Enum):
    LEFT_BTN = 1
    RIGHT_BTN = 3
    NOTHING = 0


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.default_width = width
        self.default_height = height
        self.cell_size = cell_size

        self.width = width
        self.height = height
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.seed = None
        self.update_seed()

        self.info: GameInfo

        self.mouse_state = MouseBTnState.NOTHING
        self.full_screen = False
        self.pause = True
        self.speed = speed
        self.create_on = 3
        self.remove_from = 2
        self.remove_to = 3

    def update_seed(self):
        self.seed = random.randint(0, 999999)
        random.seed(self.seed)

    def draw_lines(self) -> None:
        color = pygame.Color(220, 220, 220)

        for x in range(0, self.width + self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, color, (x, 0), (x, self.height))

        for y in range(0, self.height + self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.info = GameInfo(self.screen, True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_BACKQUOTE:
                        self.info.toggle()
                    elif event.key == K_SPACE:
                        self.pause = not self.pause
                    elif event.key == pygame.K_r:
                        self.random_all_cell()
                    elif event.key == pygame.K_BACKSPACE:
                        self.clear_all_cell()
                    # Full screen
                    elif event.key == pygame.K_f:
                        self.full_screen = not self.full_screen
                        if self.full_screen:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            display_info = pygame.display.Info()
                            self.width = display_info.current_w
                            self.height = display_info.current_h
                            self.cell_width = self.width // self.cell_size
                            self.cell_height = self.height // self.cell_size
                        else:
                            self.width = self.default_width
                            self.height = self.default_height
                            self.cell_width = self.width // self.cell_size
                            self.cell_height = self.height // self.cell_size
                            self.screen = pygame.display.set_mode((self.width, self.height))
                        # Recreate grid
                        global grid
                        grid = self.create_grid(False)
                    # Create Cell
                    elif event.key == pygame.K_a and self.create_on > 1:
                        self.create_on -= 1
                    elif event.key == pygame.K_q and self.create_on < 8:
                        self.create_on += 1
                    # Remove Cell from
                    elif event.key == pygame.K_s and self.remove_from > 0:
                        self.remove_from -= 1
                    elif event.key == pygame.K_w and self.remove_from < 8 and self.remove_from < self.remove_to:
                        self.remove_from += 1
                    # Remove Cell to
                    elif event.key == pygame.K_d and self.remove_to > 1 and self.remove_from < self.remove_to:
                        self.remove_to -= 1
                    elif event.key == pygame.K_e and self.remove_to < 8:
                        self.remove_to += 1
                    # Speed
                    elif event.key == pygame.K_MINUS and self.speed > 1:
                        self.speed -= 1
                    elif event.key == pygame.K_EQUALS and self.speed < 60:
                        self.speed += 1

                elif event.type == pygame.MOUSEMOTION:
                    self.check_mouse_motion_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_mouse_button_event(event.button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.check_mouse_button_event(MouseBTnState.NOTHING)

            self.draw_grid()
            self.draw_lines()
            if not self.pause:
                self.next_generation()
            if self.info.visible:
                self.update_info()
                self.info.draw()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

    def random_all_cell(self):
        self.update_seed()
        for row in grid:
            for cell in row:
                cell.val = random.randint(0, 1)

    def clear_all_cell(self):
        for row in grid:
            for cell in row:
                cell.val = 0

    def check_mouse_motion_event(self, event):
        if self.mouse_state != MouseBTnState.NOTHING:
            mouse_pos = event.pos
            self._check_cell_focus(mouse_pos)

    def check_mouse_button_event(self, state):
        self.mouse_state = state
        if self.mouse_state != MouseBTnState.NOTHING:
            mouse_pos = pygame.mouse.get_pos()
            self._check_cell_focus(mouse_pos)

    def _check_cell_focus(self, mouse_pos):
        x = mouse_pos[0] // self.cell_size
        y = mouse_pos[1] // self.cell_size
        cell: Cell = grid[y][x]
        cell.val = 1
        if self.mouse_state == MouseBTnState.LEFT_BTN.value:
            cell.val = 1
        if self.mouse_state == MouseBTnState.RIGHT_BTN.value:
            cell.val = 0

    @_time
    def create_grid(self, randomize: bool = False) -> list:
        # Create greed
        grid = []
        for y in range(0, self.cell_height):
            row = []
            for x in range(0, self.cell_width):
                if randomize:
                    value = random.randint(0, 1)
                else:
                    value = 0
                row.append(Cell(value, x, y, self.cell_width, self.cell_height))
            grid.append(row)

        # Find neighbours for all cells
        for row in grid:
            for cell in row:
                cell.find_neighbours(grid)

        return grid

    def draw_grid(self):
        for row in grid:
            for cell in row:
                if cell.val == 1:
                    color = pygame.Color(0, 150, 0)
                else:
                    color = pygame.Color(255, 255, 255)
                x = cell.x * self.cell_size
                y = cell.y * self.cell_size
                pygame.draw.rect(self.screen, color,
                                 (x, y, self.cell_size, self.cell_size))

    def next_generation(self):
        for row in grid:
            for cell in row:
                cell.next_val = cell.val
                count_live_neighbors = cell.count_live_neighbors()
                if cell.val == 0:
                    # B
                    if count_live_neighbors == self.create_on:
                        cell.next_val = 1
                else:
                    # S
                    if count_live_neighbors < self.remove_from or count_live_neighbors > self.remove_to:
                        cell.next_val = 0

        for row in grid:
            for cell in row:
                cell.val = cell.next_val

    def update_info(self):
        count_live = 0
        count_empty = 0
        for row in grid:
            for cell in row:
                if cell.val == 1:
                    count_live += 1
                else:
                    count_empty += 1

        self.info.update([
            f"Empty: {count_empty}",
            f"Filled: {count_live}",
            ""
            f"Speed: {self.speed}",
            f"Create: {self.create_on}",
            f"Remove: [{self.remove_from}, {self.remove_to}]",
            f"Pause: {'On' if self.pause else 'Off'}"
        ])


if __name__ == '__main__':
    game = GameOfLife(1280, 720, 5, 10)
    grid = game.create_grid(False)
    game.run()
