import pygame
from pygame import Surface

from .entity_manager import EntityManager
from ..state import State
from .pause import Pause


class Game(State):
    def __init__(self):
        super().__init__()
        self.player_score = 0
        self.em = EntityManager()

    def draw(self, screen: Surface):
        screen.fill((0, 255, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.push(Pause())
        else:
            self.em.handle_event(event)

    def update(self, delta):
        self.em.generate_events(delta)

        self.em.process_events()
