from pygame import Surface

from .asset_manager import AssetManager
from .state import State


class FrontPage(State):
    def update(self, screen: Surface):
        screen.fill((11, 11, 11))
        background = AssetManager.load_texture('front-background.png')
        screen.blit(background, (0, 0))
