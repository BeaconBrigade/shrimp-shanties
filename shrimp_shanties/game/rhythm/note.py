from enum import Enum

import pygame
from pygame import Surface, Rect

from shrimp_shanties import AssetManager, WIDTH
from shrimp_shanties.game.entity import Entity
from shrimp_shanties.game.entity_manager import PROCESS_TURN
from shrimp_shanties.game.next_id import next_entity_id


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Note(Entity):
    START_HEIGHT = 0
    BOTTOM_HEIGHT = 400

    def __init__(self, direction: Direction):
        super().__init__(next_entity_id())
        self.direction = direction
        self.height = Note.START_HEIGHT
        self.sprite = AssetManager.load_texture("up.png")
        self.sprite = pygame.transform.scale(self.sprite, (80, 80))
        self.sprite = pygame.transform.rotate(self.sprite, -90 * self.direction.value)
        print(f"new note spawned with {self.direction}")

    def register_for_events(self, em):
        pass

    def draw(self, screen: Surface):
        screen.blit(self.sprite, Rect(WIDTH / 2 - 40, self.height, 80, 80))

    def handle_event(self, event):
        if event.type == PROCESS_TURN:
            self.height += 5
            if self.height > Note.BOTTOM_HEIGHT:
                self.remove()
