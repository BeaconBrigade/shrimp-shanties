from pygame import Surface, Color

from shrimp_shanties import AssetManager
from shrimp_shanties.game import EntityManager
from shrimp_shanties.game.check.input_timing import INPUT_TIMING
from shrimp_shanties.game.entity import Entity
from shrimp_shanties.game.entity_manager import PROCESS_TURN
from shrimp_shanties.game.next_id import next_entity_id


class Score(Entity):
    def __init__(self, player_count=1):
        super().__init__(id=next_entity_id())
        self.scores = [0] * player_count
        self.misses = 0  # Initialize misses count
        self.base_font_size = 32
        self.font = None

    def draw(self, screen: Surface):
        # Calculates the font size based on the window size.
        screen_width, screen_height = screen.get_size()
        font_size = int(self.base_font_size * (screen_width / 1000))

        # Loads the font with the scaled size.
        if self.font is None or self.font.size != font_size:
            self.font = AssetManager.load_font("FiraSans-Bold.ttf", font_size)

        # Renders the points text with the scaled font size.
        score_text = self.font.render(f"Points: {self.scores[0]}", True, Color(255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.right = screen_width - 20
        score_rect.top = 30

        # Renders the misses text with the scaled font size.
        miss_text = self.font.render(f"Misses: {self.misses}", True, Color(255, 255, 255))
        miss_rect = miss_text.get_rect()
        miss_rect.right = screen_width - 20
        miss_rect.top = score_rect.bottom + 10

        screen.blit(score_text, score_rect)
        screen.blit(miss_text, miss_rect)

    def register_for_events(self, em: EntityManager):
        em.register_event(self, INPUT_TIMING)

    def handle_event(self, event):
        if event.type == INPUT_TIMING and event.success:
            self.scores[event.player_id] += int(event.score * 1000)
        elif event.type == INPUT_TIMING and not event.success:
            self.misses += 1
        elif event.type == PROCESS_TURN:
            pass
