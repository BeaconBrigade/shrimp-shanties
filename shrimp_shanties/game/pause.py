import pygame
import pygame_gui
from pygame import Surface
from pygame_gui.elements import UIPanel, UILabel, UIButton

from .. import AssetManager
from ..menu.marketplace import Marketplace
from ..state import State


class Pause(State):
    def __init__(self):
        super().__init__()

        panel = UIPanel(relative_rect=pygame.Rect((0, 40), (400, 500)), anchors={'centerx': 'centerx', 'top': 'top'},
                        object_id="#pause-panel", manager=State.MANAGER)
        self.ui_elements.append(panel)

        self.ui_elements.append(
            UILabel(relative_rect=pygame.Rect((0, 20), (-1, -1)), container=panel,
                    anchors={'centerx': 'centerx', 'top': 'top'}, text='Pause Menu', object_id='@subheading',
                    manager=State.MANAGER)
        )

        self.marketplace_button = UIButton(relative_rect=pygame.Rect((0, -100), (-1, -1)), container=panel,
                                           anchors={'center': 'center'}, text="Marketplace", object_id='#start-game',
                                           manager=State.MANAGER)
        self.ui_elements.append(self.marketplace_button)

        self.ui_elements.append(
            UIButton(relative_rect=pygame.Rect((-100, -100), (-1, -1)), container=panel,
                     anchors={'centerx': 'centerx', 'bottom': 'bottom'}, text="Launch Pad", object_id='#start-game')
        )

        self.ui_elements.append(
            UIButton(relative_rect=pygame.Rect((100, -100), (-1, -1)), container=panel,
                     anchors={'centerx': 'centerx', 'bottom': 'bottom'}, text="Continue", object_id='#start-game')
        )

    def draw(self, screen: Surface):
        # draw the parent state
        parent_surface = pygame.Surface(screen.get_size())
        parent_surface.set_alpha(255)
        self.get_parent().draw(parent_surface)

        # create a shaded copy of the parent surface
        shaded_surface = pygame.Surface(screen.get_size())
        shaded_surface.fill((0, 0, 0))
        shaded_surface.set_alpha(128)
        parent_surface.blit(shaded_surface, (0, 0))

        # Blit the shaded surface onto the main screen 
        screen.blit(parent_surface, (0, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.mixer.music.unpause()
            click = AssetManager.load_sound("button-click.wav")
            click.play()
            self.get_parent().pop()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[-3]:
            self.get_parent().push(Marketplace())
        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[-2]:
            front = self.get_parent().get_parent()
            front.get_parent().start_menu_music()
            front.pop()
            front.pop()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[-1]:
            pygame.mixer.music.unpause()
            self.get_parent().pop()
