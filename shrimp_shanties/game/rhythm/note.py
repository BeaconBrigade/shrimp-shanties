from enum import Enum

from shrimp_shanties.game.entity import Entity
from shrimp_shanties.game.next_id import next_entity_id


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Note(Entity):
    def __init__(self, direction: Direction):
        super().__init__(next_entity_id())
        self.direction = direction
        print(f"new note spawned with {self.direction}")
