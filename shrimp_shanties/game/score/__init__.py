from shrimp_shanties.game import EntityManager
from shrimp_shanties.game.check.input_timing import INPUT_TIMING
from shrimp_shanties.game.entity import Entity
from shrimp_shanties.game.entity_manager import PROCESS_TURN
from shrimp_shanties.game.next_id import next_entity_id


class Score(Entity):
    def __init__(self, player_count=1):
        super().__init__(id=next_entity_id())
        self.scores = [0] * player_count

    def register_for_events(self, em: EntityManager):
        em.register_event(self, INPUT_TIMING)

    def handle_event(self, event):
        if event.type == INPUT_TIMING:
            self.scores[event.id] += event.score * 1000
        elif event.type == PROCESS_TURN:
            pass