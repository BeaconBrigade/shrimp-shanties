from shrimp_shanties.game.player import Player, PLAYER_HIT_SPACE
from shrimp_shanties.game.check import ActiveCheck
from pygame.event import Event
import pygame


INPUT_TIMING = pygame.USEREVENT + 2


class InputTiming(ActiveCheck):
    def __init__(self, em):
        super().__init__(em)
        for entity in em.entity_list:
            if isinstance(entity, Player):
                self.player = entity
                break

        em.register_check(self, PLAYER_HIT_SPACE)

    def check(self, entity_list, event) -> Event | None:
        # TODO: find the nearest descending item to put, then do a collision check, if so return an event
        #       about increasing the score.
        print("checking for InputTiming")
        return Event(INPUT_TIMING, success=False, score=0.0, id=self.player.id)
