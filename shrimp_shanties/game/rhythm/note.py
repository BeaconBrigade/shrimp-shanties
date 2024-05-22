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
    START_HEIGHT = 0
    BOTTOM_HEIGHT = 400

    def __init__(self, note: Shrimp):
        super().__init__(next_entity_id())
        self.note = note
        self.height = Note.START_HEIGHT
        self.x = 60 + 240 * self.note.value
        file_name = f"{note.name.lower()}shrimp.png"
        self.sprite = AssetManager.load_texture(file_name)
        self.sprite = pygame.transform.scale(self.sprite, (160, 160))
        self.sprite = pygame.transform.rotate(self.sprite, -90 * random.randint(0, 3))

    def register_for_events(self, em):
        pass

    def draw(self, screen: Surface):
        screen.blit(self.sprite, Rect(self.x, self.height, 80, 80))

    def handle_event(self, event):
        if event.type == PROCESS_TURN:
            self.height += 5
            if self.height > Note.BOTTOM_HEIGHT:
                self.remove()

    def dimensions(self) -> Rect:
        return Rect(self.x, self.height, 160, 160)
