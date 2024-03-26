from pygame import Surface


class State:
    def update(self, screen: Surface):
        screen.fill((10, 10, 10))
