from pygame import Surface, Event
from pygame.event import post

from shrimp_shanties.game.next_id import next_event_id


REMOVE_ENTITY = next_event_id()


class Entity:
    def __init__(self, id):
        self.id = id

    def draw(self, screen: Surface):
        pass

    def handle_event(self, event):
        pass

    def register_for_events(self, em):
        pass

    def remove(self):
        post(Event(REMOVE_ENTITY, e_id=self.id))