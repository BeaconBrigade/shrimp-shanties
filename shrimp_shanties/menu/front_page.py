import pygame
import pygame_gui
from pygame import Surface
from pygame_gui.elements.ui_label import UILabel

from shrimp_shanties.asset_manager import AssetManager
from shrimp_shanties.menu.connection import Connection
from .. import HEIGHT
from ..state import State


class FrontPage(State):
    def __init__(self):
        super().__init__()
        self.original_background = AssetManager.load_texture('front-background.png')
        self.background = self.original_background
        self.scale_background()  # Scale the background initially
        self.start_menu_music()

        self.ui_elements.append(UILabel(relative_rect=pygame.Rect((0, HEIGHT / 8), (-1, -1)), text="Shrimp Shanties",
                                        anchors={'centerx': 'centerx', 'top': 'top'}, object_id="#title",
                                        manager=State.MANAGER))
        self.ui_elements.append(
            UILabel(relative_rect=pygame.Rect((0, HEIGHT / 3), (-1, -1)), object_id="@subheading",
                    text="Press enter to continue", anchors={'centerx': 'centerx'},
                    manager=State.MANAGER))

    def start_menu_music(self):
        AssetManager.load_music("temporary-menu.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def register_for_events(self, em):
        em.register_event(self, pygame.VIDEORESIZE)

    def draw(self, screen: Surface):
        screen.blit(self.background, (0, 0))

        # Draw rectangles behind the text elements
        for element in self.ui_elements:
            if isinstance(element, UILabel):
                text_rect = element.get_relative_rect()

                # Calculate the position and size of the rectangle
                rect_width = text_rect.width + 20
                rect_height = text_rect.height + 10
                rect_left = (screen.get_width() - rect_width) // 2  # Center horizontally
                rect_top = text_rect.top - 5

                # Draw the rectangle with a light gray color
                pygame.draw.rect(screen, (3, 68, 171), pygame.Rect(rect_left, rect_top, rect_width, rect_height))

    def propagate_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            click = AssetManager.load_sound("button-click.wav")
            click.play()
        super().propagate_event(event)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            click = AssetManager.load_sound("button-click.wav")
            click.play()
            self.push(Connection())
        elif event.type == pygame.VIDEORESIZE:
            self.scale_background()  # Scale the background when the window is resized

    def scale_background(self):
        window_width, window_height = pygame.display.get_surface().get_size()
        bg_width, bg_height = self.original_background.get_size()

        scale_x = window_width / bg_width
        scale_y = window_height / bg_height
        scale = max(scale_x, scale_y)

        new_width = int(bg_width * scale)
        new_height = int(bg_height * scale)

        self.background = pygame.transform.scale(self.original_background, (new_width, new_height))

        x = (window_width - new_width) // 2
        y = (window_height - new_height) // 2

        self.background_rect = self.background.get_rect(topleft=(x, y))
