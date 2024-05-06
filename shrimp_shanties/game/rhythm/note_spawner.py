from shrimp_shanties.game.entity import Entity
from shrimp_shanties.game.entity_manager import PROCESS_TURN
from shrimp_shanties.game.next_id import next_entity_id


class NoteSpawner(Entity):
    """ Spawn notes for a song """
    def __init__(self, shanty):
        super().__init__(next_entity_id())
        self.shanty = shanty

    def handle_event(self, event):
        if event.type == PROCESS_TURN:
            # create another note based on the song timings
            pass
