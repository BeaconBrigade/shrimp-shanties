from shrimp_shanties.game.entity import Entity
from shrimp_shanties.game.entity_manager import PROCESS_TURN
from shrimp_shanties.game.next_id import next_entity_id
from shrimp_shanties.game.rhythm.note import Note, Shrimp
from shrimp_shanties.shanty import Shanty


class NoteSpawner(Entity):
    """ Spawn notes for a song """

    def __init__(self, shanty: str):
        super().__init__(next_entity_id())
        self.shanty = Shanty(shanty)
        print(self.shanty)
        self.beat = 0
        self.em = None
        self.count = [0, 0, 0, 0, 0]

    def register_for_events(self, em):
        # this is very un-idiomatic
        self.em = em

    def handle_event(self, event):
        if event.type == PROCESS_TURN:
            # create another note based on the song timings
            dir = self.shanty.note(self.beat)
            if dir is not None:
                self.count[dir.value] += 1
                self.em.add_entity(Note(dir))
                print('\033[2J\033[H', end='')
                print(f"Red: {self.count[Shrimp.RED.value]}, Yellow: {self.count[Shrimp.YELLOW.value]}, "
                    f"Green: {self.count[Shrimp.GREEN.value]}, Blue: {self.count[Shrimp.BLUE.value]}, Hang: {self.count[Shrimp.HANG.value]}")
            self.beat += 1
