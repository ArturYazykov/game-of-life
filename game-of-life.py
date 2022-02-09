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
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.seed = None
        self.update_seed()

        self.info: GameInfo

        self.speed = speed
        self.mouse_state = MouseBTnState.NOTHING
        self.pause = False

    def update_seed(self):
        self.seed = random.randint(0, 999999)
        random.seed(self.seed)

    def draw_lines(self) -> None:
        for x in range(0, self.width + self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color(200, 200, 200),
                             (x, 0), (x, self.height))

        for y in range(0, self.height + self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color(200, 200, 200),
                             (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.info = GameInfo(self.screen)

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
            if self.info.is_visible:
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
        print(mouse_pos)
        x = mouse_pos[0] // self.cell_size
        y = mouse_pos[1] // self.cell_size
        cell: Cell = grid[y][x]
        cell.val = 1
        if self.mouse_state == MouseBTnState.LEFT_BTN.value:
            cell.val = 1
        if self.mouse_state == MouseBTnState.RIGHT_BTN.value:
            cell.val = 0
        print(y, x)

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
                if cell.val == 1:
                    if count_live_neighbors < 2 or count_live_neighbors > 3:
                        cell.next_val = 0
                else:
                    if count_live_neighbors == 3:
                        cell.next_val = 1

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
            f"Seed: {self.seed}   Filled: {count_live}    Empty: {count_empty}",
            f"Pouse: {'On' if self.pause else 'Off'}"
        ])


if __name__ == '__main__':
    game = GameOfLife(1280, 740, 10, 10)
    grid = game.create_grid(False)
    game.run()
