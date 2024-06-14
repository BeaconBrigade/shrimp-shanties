from pygame.event import post, Event

from shrimp_shanties.game.entity import Entity
from shrimp_shanties.game.entity_manager import PROCESS_TURN
from shrimp_shanties.game.next_id import next_entity_id, next_event_id
from shrimp_shanties.game.rhythm.note import Note, Shrimp
from shrimp_shanties.shanty import Shanty, SongOver

SONG_OVER = next_event_id()


class NoteSpawner(Entity):
    """ Spawn notes for a song """

    def __init__(self, shanty: Shanty):
        super().__init__(next_entity_id())
        self.shanty = shanty
        print(self.shanty)
        self.beat = 0
        self.em = None
        self.count = [0, 0, 0, 0, 0]

    def register_for_events(self, em):
        # this is very un-idiomatic
        self.em = em

    def handle_event(self, event):
        if event.type == PROCESS_TURN:
            change_in_beats = 60 * event.delta
            elapsed_beats = range(round(self.beat), round(self.beat + change_in_beats))
            # print(f"start={self.beat:04} change={change_in_beats:04} elapsed={list(elapsed_beats)}")
            # create another note based on the song timings
            for beat in elapsed_beats:
                try:
                    dirs = self.shanty.note(beat)
                    if dirs is not None:
                        for dir in dirs:
                            self.count[dir.value] += 1
                            self.em.add_entity(Note(dir))
                            print('\033[2J\033[H', end='')
                            print(f"Red: {self.count[Shrimp.RED.value]}, Yellow: {self.count[Shrimp.YELLOW.value]}, "
                                  f"Green: {self.count[Shrimp.GREEN.value]}, Blue: {self.count[Shrimp.BLUE.value]}")
                except SongOver:
                    for entity in self.em.entity_list:
                        if isinstance(entity, Note):
                            break
                    else:
                        post(Event(SONG_OVER, out_of=sum(self.count) * 1000))
            self.beat += change_in_beats
