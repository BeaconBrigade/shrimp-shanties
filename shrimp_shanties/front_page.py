import pygame
from pygame_gui.elements.ui_label import UILabel
from pygame import Surface

from . import HEIGHT
from .asset_manager import AssetManager
from .connection import Connection
from .state import State


class FrontPage(State):
    def __init__(self):
        super().__init__()
        self.background = AssetManager.load_texture('front-background.png')

        self.ui_elements.append(UILabel(relative_rect=pygame.Rect((0, -10), (-1, -1)), text="Shrimp Shanties",
                                        anchors={'center': 'center'}, object_id="#title", manager=State.MANAGER))
        self.ui_elements.append(
            UILabel(relative_rect=pygame.Rect((0, HEIGHT / 2 + 80), (-1, -1)), object_id="#subheading",
                    text="Press enter to continue", anchors={'centerx': 'centerx'},
                    manager=State.MANAGER))

    def update(self, screen: Surface):
        screen.blit(self.background, (0, 0))

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RETURN] or pressed[pygame.K_SPACE]:
            self.push(Connection())
