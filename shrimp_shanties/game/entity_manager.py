from shrimp_shanties.game.check import ActiveCheck, PassiveCheck
from shrimp_shanties.game.entity import Entity, REMOVE_ENTITY
from pygame.event import Event

from shrimp_shanties.game.next_id import next_event_id


PROCESS_TURN = next_event_id()


class EntityManager:
    def __init__(self):
        self.entity_list: list[Entity] = []
        self.event_map: dict[int, list[Entity]] = dict()
        self.event_checks: list[PassiveCheck] = []
        self.event_list: list[Event] = []
        self.check_map: dict[int, list[ActiveCheck]] = dict()

    # two ways events are sent to entities:
    # (1) events coming from pygame
    # (2) events that are created by some function such as a collision check
    def generate_events(self, delta):
        for check in self.event_checks:
            e = check.check(delta, self.entity_list)
            if e is not None:
                self.event_list.append(e)

    def process_events(self, delta):
        self.event_list.append(Event(PROCESS_TURN, delta=delta))
        for event in self.event_list:
            entities = self.event_map.get(event.type)
            if entities is not None:
                for entity in entities:
                    if entity is not None:
                        entity.handle_event(event)
            checks = self.check_map.get(event.type)
            if checks is None:
                continue
            for check in checks:
                e = check.check(self.entity_list, event)
                if e is not None:
                    self.event_list.append(e)

        self.event_list.clear()

    def handle_event(self, event):
        if self.event_map.get(event.type) is not None or self.check_map.get(event.type) is not None:
            self.event_list.append(event)
        elif event.type == REMOVE_ENTITY:
            self.remove_entity(event.e_id)

    def draw(self, screen):
        for entity in self.entity_list:
            entity.draw(screen)

    def add_entity(self, entity: Entity):
        entity.register_for_events(self)
        self.register_event(entity, PROCESS_TURN)
        self.entity_list.append(entity)

    def remove_entity(self, search_id):
        for i, entity in enumerate(self.entity_list):
            if entity.id == search_id:
                del self.entity_list[i]

    def register_event(self, entity, type):
        if type not in self.event_map:
            self.event_map[type] = []
        self.event_map[type].append(entity)

    def unregister_event(self, entity: Entity, type):
        if self.event_map.get(type) is not None:
            self.event_map[type].remove(entity)

    def register_check(self, check: ActiveCheck, type):
        """ Register an active check so the check will be called when an event is received """
        if self.check_map.get(type) is not None:
            self.check_map[type] += check
        else:
            self.check_map[type] = [check]

    def unregister_check(self, check: ActiveCheck, type):
        if self.check_map.get(type) is not None:
            self.check_map[type].remove(check)

    def register_passive_check(self, check: PassiveCheck):
        self.event_checks += check

    def unregister_passive_check(self, check: PassiveCheck):
        self.event_checks.remove(check)
