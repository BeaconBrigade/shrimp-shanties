from shrimp_shanties.game.next_id import next_event_id
from shrimp_shanties.game.player import Player, PLAYER_HIT_SPACE
from shrimp_shanties.game.check import ActiveCheck
from pygame.event import Event


INPUT_TIMING = next_event_id()


class InputTiming(ActiveCheck):
    def __init__(self, em):
        super().__init__(em)
        for entity in em.entity_list:
            if isinstance(entity, Player):
                self.player = entity
                break

        em.register_check(self, PLAYER_HIT_SPACE)

    def check(self, entity_list, event) -> Event | None:
        # Finds the nearest descending item.
        nearest_item = None
        min_distance = float('inf')
        for entity in entity_list:
            if hasattr(entity, 'is_descending') and entity.is_descending:
                distance = abs(self.player.rect.y - entity.rect.y)
                if distance < min_distance:
                    min_distance = distance
                    nearest_item = entity
        # Performs a collision check.
        if nearest_item and self.player.rect.colliderect(nearest_item.rect):
            # Returns an event for increasing the score
            print("Collision detected with item:", nearest_item)
            return Event(INPUT_TIMING, success=True, score=10.0, id=self.player.id)
        print("checking for InputTiming")
        return Event(INPUT_TIMING, success=False, score=0.0, id=self.player.id)
