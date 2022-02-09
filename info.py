import pygame
from pygame.rect import Rect
from pygame.surface import Surface


class GameInfo:
    def __init__(self, screen: Surface, visible=False) -> None:
        self.screen = screen

        self.visible = visible

        self.background_rect = Rect(0, 0, 0, 0)
        self.background_color_alpha = (255, 255, 255, 150)

        self.color = (25, 25, 25)
        self.font = pygame.font.Font(None, 24)
        self.lines = None

        self.default_text = [
            "Hot keys:",
            "   [~] - Hide/Show this menu",
            "   ESCAPE - Exit game",
            "   SPACE - Pause",
            "   BACKSPACE - Clear greed",
            "   R - Generate random greed",
            "Working only in Pause(SPACE) mode!",
            "   LEFT Mouse Button - Fills a cell",
            "   RIGHT Mouse Button - Clears a cell",
            ""
        ]

        self._update_text([])

    def toggle(self):
        self.visible = not self.visible

    def update(self, text_lines: list):
        if self.visible:
            self._update_text(text_lines)

    def _update_text(self, text_lines: list):
        self.lines = []
        left = 20
        top = 20
        right = 0
        for text in (self.default_text + text_lines):
            line: Surface = self.font.render(text, True, self.color)
            rect = Rect(left, top, line.get_rect().w, line.get_rect().h)
            self.lines.append((line, rect))
            top += 30

            # Find max width
            if right < line.get_rect().w:
                right = line.get_rect().w

        self.background_rect.update(10, 10, right + 20, self.lines[-1][1].bottom)

    def draw(self):
        if self.visible:
            self._draw_rect_alpha()
            self._draw_text()

    def _draw_rect_alpha(self):
        shape_surf = pygame.Surface(self.background_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, self.background_color_alpha, shape_surf.get_rect())
        self.screen.blit(shape_surf, self.background_rect)

    def _draw_text(self):
        for line in self.lines:
            self.screen.blit(line[0], line[1])
