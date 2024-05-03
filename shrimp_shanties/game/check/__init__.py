from pygame.event import Event


class PassiveCheck:
    """ Check that is run each frame and doesn't require any other events """

    def check(self, delta, entity_list):
        pass


class ActiveCheck:
    """ Check that is run based on an event, potentially generating a new event """

    def __init__(self, em):
        pass

    def check(self, entity_list, event) -> Event | None:
        pass
