from shrimp_shanties.game import EntityManager
from shrimp_shanties.game.check.input_timing import INPUT_TIMING
from shrimp_shanties.game.entity import Entity


class Score(Entity):
    def __init__(self, player_count=1):
        super().__init__(id=0xfabb)
        self.scores = [0] * player_count

    def register_for_events(self, em: EntityManager):
        em.register_event(self, INPUT_TIMING)

    def handle_event(self, event):
        if event.type == INPUT_TIMING:
            self.scores[event.id] += event.score * 1000
