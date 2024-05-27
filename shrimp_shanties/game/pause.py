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
        # Get the current window dimensions
        window_width, window_height = screen.get_size()
        
        # Create a shaded surface the same size as the window
        shaded_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        shaded = pygame.Color((0, 255, 0)).lerp((32, 20, 46), 0.5)
        shaded_surface.fill(shaded)
        
        # Draw the parent state onto a temporary surface
        parent_surface = pygame.Surface((window_width, window_height))
        self.get_parent().draw(parent_surface)

        # Create a shaded copy of the parent surface  
        shaded_surface = parent_surface.copy()
        shaded = pygame.Color((255, 255, 255)).lerp((10, 5, 10), 0.2)
        shaded_surface.fill(shaded, special_flags=pygame.BLEND_RGBA_MULT)

        # Blit the shaded surface onto the main screen 
        screen.blit(shaded_surface, (0, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.get_parent().pop()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[-2]:
            self.get_parent().pop()  
        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[-1]:
            front = self.get_parent().get_parent()
            front.pop()
            front.pop()