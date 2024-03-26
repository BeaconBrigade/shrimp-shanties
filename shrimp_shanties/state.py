from pygame import Surface


class State:
    BASE = None

    def __init__(self):
        self.child = None

    def update(self, screen: Surface):
        screen.fill((10, 10, 10))
        if self.child is not None:
            self.child.update(screen)

    def push(self, child):
        if self.child is None:
            self.child = child
        else:
            self.child.push(child)

    def pop(self):
        if self.child is not None:
            if self.child.child is None:
                self.child = None
            else:
                self.child.pop()
