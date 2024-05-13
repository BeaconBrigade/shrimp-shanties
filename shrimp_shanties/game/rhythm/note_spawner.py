from shrimp_shanties.game.entity import Entity
from shrimp_shanties.game.entity_manager import PROCESS_TURN
from shrimp_shanties.game.next_id import next_entity_id
from shrimp_shanties.game.rhythm.note import Note
from shrimp_shanties.shanty import Shanty


class NoteSpawner(Entity):
    """ Spawn notes for a song """
    def __init__(self, shanty: str):
        super().__init__(next_entity_id())
        self.shanty = Shanty(shanty)
        print(self.shanty)
        self.beat = 0
        self.em = None

    def register_for_events(self, em):
        # this is very un-idiomatic
        self.em = em

    def handle_event(self, event):
        if event.type == PROCESS_TURN:
            # create another note based on the song timings
            dir = self.shanty.note(self.beat)
            if dir is not None:
                self.em.add_entity(Note(dir))
            self.beat += 1

