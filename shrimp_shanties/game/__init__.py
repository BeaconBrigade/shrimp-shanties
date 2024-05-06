import pygame
from pygame import Surface

from .check.input_timing import InputTiming
from .entity_manager import EntityManager
from .player import Player
from .rhythm.note_spawner import NoteSpawner
from .score import Score
from ..state import State
from .pause import Pause


class Game(State):
    def __init__(self, shanty):
        super().__init__()
        self.player_score = 0
        self.em = EntityManager()
        self.em.add_entity(Player())
        self.em.add_entity(Score())
        self.em.add_entity(NoteSpawner(shanty))
        InputTiming(self.em)

    def draw(self, screen: Surface):
        screen.fill((0, 255, 0))
        self.em.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.push(Pause())
        else:
            self.em.handle_event(event)

    def update(self, delta):
        self.em.generate_events(delta)

        self.em.process_events()
