from shrimp_shanties.game.entity import Entity


class EntityManager:
    def __init__(self):
        self.entity_list = []
        self.event_map = dict()
        self.event_checks = []
        self.event_list = []

    # two ways events are sent to entities:
    # (1) events coming from pygame
    # (2) events that are created by some function such as a collision check
    def generate_events(self, delta):
        for check in self.event_checks:
            e = check.check(delta, self.entity_list)
            if e is not None:
                self.event_list.append(e)

    def process_events(self):
        for event in self.event_list:
            entity = self.event_map.get(event.type)
            if entity is not None:
                entity.handle_event(event)

        self.event_list.clear()

    def handle_event(self, event):
        if self.event_map.get(event.type) is not None:
            self.event_list.append(event)

    def draw(self, screen):
        for entity in self.entity_list:
            entity.draw(screen)

    def add_entity(self, entity: Entity):
        self.entity_list.append(entity)

    def remove_entity(self, search_id):
        for i, entity in enumerate(self.entity_list):
            if entity.id == search_id:
                del self.entity_list[search_id]
