import random
from datetime import datetime

import pygame
from pygame.locals import *

from cell import Cell


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.speed = speed
        self.mouse_down = False

    def draw_lines(self) -> None:
        for x in range(0, self.width + self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))

        for y in range(0, self.height + self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    self.check_mouse_motion_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_mouse_button_event(True)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.check_mouse_button_event(False)

            self.draw_grid()
            self.draw_lines()
            self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

    def check_mouse_motion_event(self, event):
        if self.mouse_down:
            mouse_pos = event.pos
            self._check_cell_focus(mouse_pos)

    def check_mouse_button_event(self, down):
        self.mouse_down = down
        if self.mouse_down:
            mouse_pos = pygame.mouse.get_pos()
            self._check_cell_focus(mouse_pos)

    def _check_cell_focus(self, mouse_pos):
        # TODO
        pass

    def create_grid(self, randomize: bool = False) -> list:
        start = datetime.now()
        # Create greed
        grid = []
        for y in range(0, self.cell_height):
            for x in range(0, self.cell_width):
                if randomize:
                    value = random.randint(0, 1)
                else:
                    value = 0
                grid.append(Cell(value, x, y, self.cell_width, self.cell_height))

        # Find neighbours for all cells
        for cell in grid:
            cell.find_neighbours(grid)

        # 13.806975
        delta = datetime.now() - start
        print(delta)
        return grid

    def draw_grid(self):
        for cell in grid:
            if cell.val == 1:
                color = pygame.Color(0, 150, 0)
            else:
                color = pygame.Color(255, 255, 255)
            x = cell.x * self.cell_size
            y = cell.y * self.cell_size
            pygame.draw.rect(self.screen, color,
                             (x, y, self.cell_size, self.cell_size))

    def get_next_generation(self):
        for cell in grid:
            count_live_neighbors = cell.count_live_neighbors()
            if cell.val == 1:
                if count_live_neighbors < 2 or count_live_neighbors > 3:
                    cell.next_val = 0
            else:
                if count_live_neighbors == 3:
                    cell.next_val = 1

        count_live = 0
        count_empty = 0
        for cell in grid:
            cell.val = cell.next_val
            if cell.val == 1:
                count_live += 1
            else:
                count_empty += 1

        print(f"Seed: {seed} Generation: {0} Live: {count_live} Empty: {count_empty}")


if __name__ == '__main__':
    # Seed: 153
    # Seed: 1526
    # Seed: 1730
    # Seed: 1001
    seed = random.randint(1000, 2000)
    random.seed(seed)
    game = GameOfLife(1280, 740, 10, 10)
    grid = game.create_grid(randomize=True)
    # pp(grid)
    game.run()
