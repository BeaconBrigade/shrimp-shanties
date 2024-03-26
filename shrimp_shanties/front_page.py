import pygame
from pygame import Surface

from .asset_manager import AssetManager
from .connection import Connection
from .state import State


class FrontPage(State):
    def update(self, screen: Surface):
        if self.child is not None:
            self.child.update(screen)
            return
        background = AssetManager.load_texture('front-background.png')
        screen.blit(background, (0, 0))
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                self.push(Connection())
