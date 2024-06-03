from pygame import Surface, Color
from pygame.event import post, Event

from shrimp_shanties import AssetManager
from shrimp_shanties.game import EntityManager
from shrimp_shanties.game.check.input_timing import INPUT_TIMING
from shrimp_shanties.game.entity import Entity
from shrimp_shanties.game.entity_manager import PROCESS_TURN
from shrimp_shanties.game.next_id import next_entity_id, next_event_id
from shrimp_shanties.game.rhythm.note_spawner import SONG_OVER

END_INFO = next_event_id()

import pygame


class Score(Entity):
    def __init__(self, player_count=1):
        super().__init__(id=next_entity_id())
        self.scores = [0] * player_count
        self.misses = 0  # Initialize misses count
        self.base_font_size = 32
        self.font = None
        self.score_rect = None
        self.miss_rect = None

    def draw(self, screen: Surface):
        # Calculates the font size based on the window size.
        screen_width, screen_height = screen.get_size()
        font_size = int(self.base_font_size * min(screen_width / 600, screen_height / 800))

        # Loads the font with the scaled size.
        if self.font is None or self.font.size != font_size:
            self.font = AssetManager.load_font("FiraSans-Bold.ttf", font_size)

        # Renders the points text with the scaled font size.
        score_text = self.font.render(f"Points: {self.scores[0]}", True, Color(255, 255, 255))
        self.score_rect = score_text.get_rect()
        self.score_rect.left = screen_width * 0.025
        self.score_rect.top = screen_height * 0.025

        # Renders the misses text with the scaled font size.
        miss_text = self.font.render(f"Misses: {self.misses}", True, Color(255, 255, 255))
        self.miss_rect = miss_text.get_rect()
        self.miss_rect.right = screen_width * 0.975
        self.miss_rect.top = screen_height * 0.025

        screen.blit(score_text, self.score_rect)
        screen.blit(miss_text, self.miss_rect)

    def register_for_events(self, em: EntityManager):
        em.register_event(self, INPUT_TIMING)
        em.register_event(self, pygame.VIDEORESIZE)
        em.register_event(self, SONG_OVER)

    def handle_event(self, event):
        if event.type == INPUT_TIMING and event.success:
            self.scores[event.player_id] += int(event.score * 1000)
        elif event.type == INPUT_TIMING and not event.success:
            self.misses += 1
        elif event.type == SONG_OVER:
            post(Event(END_INFO, score=self.scores[0], misses=self.misses, percent=100 * self.scores[0] / event.out_of))
        elif event.type == pygame.VIDEORESIZE:
            # Reset the font when the window is resized
            self.font = None
        elif event.type == PROCESS_TURN:
            pass
