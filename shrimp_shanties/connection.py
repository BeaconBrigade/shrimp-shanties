import pygame
from pygame import Surface

from shrimp_shanties.state import State


class Connection(State):
    def update(self, screen: Surface):
        screen.fill((255, 0, 0))

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            State.BASE.pop()
