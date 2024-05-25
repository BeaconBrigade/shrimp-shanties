from enum import Enum

import pygame
import random
from pygame import Surface, Rect

from shrimp_shanties.game.entity.hitbox import Hitbox
from shrimp_shanties import AssetManager
from shrimp_shanties.game.entity_manager import PROCESS_TURN
from shrimp_shanties.game.next_id import next_entity_id


class Shrimp(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2
    BLUE = 3


class Note(Hitbox):
    def __init__(self, note: Shrimp):
        super().__init__(next_entity_id())
        self.note = note
        self.height_ratio = 0.0
        self.x_ratio = (70 + 250 * self.note.value) / 1000
        file_name = f"{note.name.lower()}shrimp.png"
        self.original_sprite = AssetManager.load_texture(file_name)
        self.sprite = self.original_sprite
        self.sprite = pygame.transform.rotate(self.sprite, -90 * random.randint(0, 3))
        self.height = 0
        self.scale_sprite()  # Scales the sprite to window size when spawning.

    def register_for_events(self, em):
        em.register_event(self, pygame.VIDEORESIZE)

    def draw(self, screen: Surface):
        screen_width, screen_height = screen.get_size()
        x = int(self.x_ratio * screen_width)
        y = int(self.height_ratio * screen_height)
        screen.blit(self.sprite, Rect(x, y, self.sprite.get_width(), self.sprite.get_height()))

    def handle_event(self, event):
        if event.type == PROCESS_TURN:
            self.height_ratio += 0.01
            if self.height_ratio > 0.8:
                self.remove()
        elif event.type == pygame.VIDEORESIZE:
            self.scale_sprite()  # Scales the spawned sprites when the window is resized.

    def dimensions(self) -> Rect:
        screen_width, screen_height = pygame.display.get_surface().get_size()
        x = int(self.x_ratio * screen_width)
        y = int(self.height_ratio * screen_height)
        return Rect(x, y, self.sprite.get_width(), self.sprite.get_height())

    def scale_sprite(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        scale_factor = min(screen_width*4 / 1000, screen_height*4 / 600)
        new_width = int(self.original_sprite.get_width() * scale_factor)
        new_height = int(self.original_sprite.get_height() * scale_factor)
        self.sprite = pygame.transform.scale(self.original_sprite, (new_width, new_height))

