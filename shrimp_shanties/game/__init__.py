import pygame
from pygame import Surface

from .check.input_timing import InputTiming
from .entity_manager import EntityManager
from .over import Over
from .pause import Pause
from .player import Player
from .rhythm.note_spawner import NoteSpawner
from .score import Score, END_INFO
from .. import AssetManager
from ..shanty import Shanty
from ..state import State


class Game(State):
    def __init__(self, shanty):
        super().__init__()
        self.player_score = 0
        self.em = EntityManager()
        self.em.add_entity(Player())
        self.em.add_entity(Score())
        shanty = Shanty(shanty)
        self.em.add_entity(NoteSpawner(shanty))
        InputTiming(self.em)
        if shanty.audio_name != "":
            AssetManager.load_shanty_music(shanty.file_name, shanty.audio_name)
            pygame.mixer.music.play(-1)

    def draw(self, screen: Surface):
        screen.fill((0, 255, 0))
        self.em.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.mixer.music.pause()
            self.push(Pause())
        elif event.type == END_INFO:
            pygame.mixer.music.pause()
            self.push(Over(event.score, event.misses, event.percent))
        else:
            self.em.handle_event(event)

    def update(self, delta):
        if self.child is None:
            self.em.generate_events(delta)

            self.em.process_events(delta)
        else:
            self.child.update(delta)
