import pygame
from pygame import Surface

from ..state import State
from .pause import Pause


class Game(State):
    def __init__(self):
        super().__init__()
        self.player_score = 0

    def draw(self, screen: Surface):
        screen.fill((0, 255, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.push(Pause())
