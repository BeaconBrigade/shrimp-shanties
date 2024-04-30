from pygame import Surface


class State:
    BASE = None
    MANAGER = None

    def __init__(self, depth=0):
        self.child = None
        self.ui_elements = []
        self.depth = depth

    def propagate_draw(self, screen: Surface):
        if self.child is not None:
            self.child.propagate_draw(screen)
        else:
            self.draw(screen)

    def draw(self, screen: Surface):
        screen.fill((10, 10, 10))

    def propagate_event(self, event):
        if self.child is not None:
            self.child.propagate_event(event)
        else:
            self.handle_event(event)

    def handle_event(self, event):
        pass

    def update(self, delta):
        if self.child is not None:
            self.child.update(delta)

    def push(self, child):
        if self.child is None:
            child.depth = self.depth + 1
            self.child = child
            self.deactivate_ui()
        else:
            self.child.push(child)

    def pop(self):
        if self.child is not None:
            if self.child.child is None:
                self.child = None
                self.reactivate_ui()
            else:
                self.child.pop()

    def get_parent(self):
        parent = State.BASE
        depth = self.depth - 1
        while depth > 0:
            parent = parent.child
            depth -= 1

        return parent

    def reactivate_ui(self):
        for ui in self.ui_elements:
            ui.show()

    def deactivate_ui(self):
        for ui in self.ui_elements:
            ui.hide()

    def __del__(self):
        for ui in self.ui_elements:
            ui.kill()
