import pygame
from pygame import Surface
from pygame_gui.elements import UILabel

from .. import AssetManager
from ..state import State
from shrimp_shanties.game import Game, Pause


class Startup(State):
    def __init__(self, shanty):
        super().__init__()
        self.game = Game(shanty)
        self.delta = None
        self.counter = 4

        beep = AssetManager.load_sound("low-beep.wav")
        beep.play()

        self.ui_elements.append(
            UILabel(relative_rect=pygame.Rect((0, 0), (-1, -1)),
                    anchors={'center': 'center'}, text=str(self.counter - 1), object_id='#title',
                    manager=State.MANAGER)
        )

    def update(self, delta):
        if self.child is not None:
            self.child.update(delta)
            return

        # calculate current counter position using rounding
        if self.delta is None:
            self.delta = delta
        else:
            self.delta += delta
        self.counter -= int(self.delta)

        # update text, and move onto the game
        if self.counter > 1:
            self.ui_elements[0].set_text(str(self.counter - 1))
        elif self.counter == 1:
            self.ui_elements[0].set_text("Go!")
        elif self.counter < 1:
            self.get_parent().pop()
            self.get_parent().push(self.game)
            return

        # play sound effects
        if self.delta >= 1:
            self.delta -= 1
            if self.counter > 1:
                beep = AssetManager.load_sound("low-beep.wav")
            else:
                beep = AssetManager.load_sound("high-beep.wav")
                beep.set_volume(0.4)
            beep.play()

    def draw(self, screen: Surface):
        game_surface = pygame.Surface(screen.get_size())
        game_surface.set_alpha(255)
        self.game.draw(game_surface)

        shaded_surface = pygame.Surface(screen.get_size())
        shaded_surface.fill((0, 0, 0))
        shaded_surface.set_alpha(128)
        game_surface.blit(shaded_surface, (0, 0))

        screen.blit(game_surface, (0, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.push(Pause())
