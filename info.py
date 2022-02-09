import pygame
from pygame.rect import Rect
from pygame.surface import Surface


class GameInfo:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen

        self.show = False

        self.color = (0, 0, 0)
        self.font = pygame.font.Font(None, 24)
        self.lines = None

        self.text = [
            "Hot keys:",
            "   ESCAPE - Exit game",
            "   SPACE - Pause",
            "   BACKSPACE - Clear greed",
            "   R - Generate random greed",
            "Working only in Pause(SPACE) mode!",
            "   LEFT Mouse Button - Fills a cell",
            "   RIGHT Mouse Button - Clears a cell",
            ""
        ]

        self.init()

    def init(self):
        self._update_text([])

    def update(self, text_lines: list):
        if self.show:
            self._update_text(text_lines)

    def draw(self):
        if self.show:
            for line in self.lines:
                self.screen.blit(line[0], line[1])

    def toggle(self):
        self.show = not self.show

    @property
    def is_visible(self):
        return self.show

    def _update_text(self, text_lines: list):
        self.lines = []
        left = 20
        top = 20
        for text in (self.text + text_lines):
            line: Surface = self.font.render(text, True, self.color)
            rect = Rect(left, top, line.get_rect().w, line.get_rect().h)
            self.lines.append((line, rect))
            top += 40
