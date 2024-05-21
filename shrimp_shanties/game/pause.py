import pygame
import pygame_gui
from pygame import Surface
from pygame_gui.elements import UIPanel, UILabel, UIButton

from .. import HEIGHT, WIDTH
from ..state import State


class Pause(State):
    def __init__(self):
        super().__init__()

        panel = UIPanel(relative_rect=pygame.Rect((0, 40), (400, 500)), anchors={'centerx': 'centerx', 'top': 'top'},
                        object_id="#pause-panel", manager=State.MANAGER)
        self.ui_elements.append(panel)

        self.ui_elements.append(
            UILabel(relative_rect=pygame.Rect((0, 20), (-1, -1)), container=panel,
                    anchors={'centerx': 'centerx', 'top': 'top'}, text='Pause', object_id='@subheading',
                    manager=State.MANAGER)
        )

        self.ui_elements.append(
            UIButton(relative_rect=pygame.Rect((-100, -100), (-1, -1)), container=panel,
                     anchors={'centerx': 'centerx', 'bottom': 'bottom'}, text="Continue", object_id='#start-game')
        )

        self.ui_elements.append(
            UIButton(relative_rect=pygame.Rect((100, -100), (-1, -1)), container=panel,
                     anchors={'centerx': 'centerx', 'bottom': 'bottom'}, text="Back", object_id='#start-game')
        )

    def draw(self, screen: Surface):
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.get_parent().draw(s)
        shaded = pygame.Color((0, 255, 0)).lerp((32, 20, 46), 0.5)
        s.fill(shaded)
        screen.blit(s, (0, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.get_parent().pop()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[-2]:
            self.get_parent().pop()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[-1]:
            front = self.get_parent().get_parent().get_parent()
            front.pop()
            front.pop()
            
