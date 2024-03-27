import pygame
from pygame import Surface

from . import WIDTH, HEIGHT
from .asset_manager import AssetManager
from .connection import Connection
from .state import State


class FrontPage(State):
    def __init__(self):
        super().__init__()
        self.background = AssetManager.load_texture('front-background.png')
        title_font = AssetManager.load_font('FiraSans-Bold.ttf', 80)
        sub_font = AssetManager.load_font('FiraSans-Bold.ttf', 20)
        self.title = title_font.render('Shrimp Shanties!', True, (235, 247, 238))
        self.sub = sub_font.render('Press enter to continue', True, (204, 204, 204))

    def update(self, screen: Surface):
        if self.child is not None:
            self.child.update(screen)
            return
        screen.blit(self.background, (0, 0))
        screen.blit(self.title, (WIDTH / 2 - 295, HEIGHT / 2 - 50))
        screen.blit(self.sub, (WIDTH / 2 - 100, HEIGHT / 2 + 100))

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RETURN] or pressed[pygame.K_SPACE]:
            self.push(Connection())
