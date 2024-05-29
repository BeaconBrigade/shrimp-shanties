import pygame
import pygame_gui
from pygame import Surface
from pygame_gui.elements import UILabel, UIButton, UIPanel, UIImage

from shrimp_shanties.state import State
from shrimp_shanties.game import Game
from shrimp_shanties.asset_manager import AssetManager

import os
from pathlib import Path

class Marketplace(State):
    def __init__(self):
        super().__init__()
        self.load_image_assets()
        self.ui_elements.append(UILabel(relative_rect=pygame.Rect((0, 0), (-1, -1)), object_id="@subheading",
                                        text="Marketplace Test", anchors={'centerx': 'centerx', 'top': 'top'},
                                        manager=State.MANAGER))

        self.ui_elements.append(UIButton(relative_rect=pygame.Rect((0, 50), (-1, -1)), object_id="#return", 
                                        text="Back", anchors={'centerx': 'centerx', 'top': 'top'},
                                        manager=State.MANAGER))

    def load_image_assets(self):
        image_files = AssetManager.list_cosmetics()

        self.image_assets = []
        for image_file in image_files:
            image = AssetManager.load_cosmetic(image_file)
            self.image_assets.append(image)

        self.create_image_panels()

    def create_image_panels(self):
        panel_width = 200
        panel_height = 200
        spacing = 20

        for i, image in enumerate(self.image_assets):
            x = (i % 3) * (panel_width + spacing) + spacing
            y = (i // 3) * (panel_height + spacing) + spacing

            panel = UIPanel(relative_rect=pygame.Rect((x, y+100), (panel_width, panel_height)),
                        manager=State.MANAGER, anchors={'left': 'left', 'top': 'top'})

            image_element = UIImage(relative_rect=pygame.Rect((0, 0), (panel_width, panel_height)),
                                image_surface=image, manager=State.MANAGER,
                                container=panel, anchors={'centerx': 'centerx', 'centery': 'centery'})

            self.ui_elements.append(panel)
            self.ui_elements.append(image_element)

    def draw(self, screen: Surface):
        screen.fill((30, 30, 50))

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[-1]:
            self.get_parent().pop()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.get_parent().pop()
        elif event.type == pygame.KEYDOWN:
            self.get_parent().pop()