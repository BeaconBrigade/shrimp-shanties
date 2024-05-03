from pygame import Surface


class Entity:
    def __init__(self, id):
        self.id = id

    def draw(self, screen: Surface):
        pass

    def handle_event(self, event):
        pass

    def register_for_events(self, em):
        pass
