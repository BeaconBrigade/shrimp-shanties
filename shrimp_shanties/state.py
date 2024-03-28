from pygame import Surface


class State:
    BASE = None
    MANAGER = None

    def __init__(self):
        self.child = None
        self.ui_elements = []

    def update_state(self, screen: Surface):
        if self.child is not None:
            self.child.update_state(screen)
        else:
            self.update(screen)

    def update(self, screen: Surface):
        screen.fill((10, 10, 10))

    def push(self, child):
        if self.child is None:
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

    def reactivate_ui(self):
        for ui in self.ui_elements:
            ui.show()

    def deactivate_ui(self):
        for ui in self.ui_elements:
            ui.hide()
