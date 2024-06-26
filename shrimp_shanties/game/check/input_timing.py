import pygame
from pygame.event import Event

from shrimp_shanties import AssetManager
from shrimp_shanties.game.check import ActiveCheck
from shrimp_shanties.game.next_id import next_event_id
from shrimp_shanties.game.player import Player
from shrimp_shanties.game.rhythm.note import Note, Shrimp

INPUT_TIMING = next_event_id()


class InputTiming(ActiveCheck):
    def __init__(self, em):
        super().__init__(em)
        for entity in em.entity_list:
            if isinstance(entity, Player):
                self.player = entity
                break

        em.register_check(self, pygame.KEYDOWN)

    def check(self, entity_list, event) -> Event | None:
        shrimp_key_mapping = {
            pygame.K_d: Shrimp.RED,
            pygame.K_f: Shrimp.YELLOW,
            pygame.K_j: Shrimp.GREEN,
            pygame.K_k: Shrimp.BLUE
        }
        if event.key not in shrimp_key_mapping:
            return None

        shrimp = shrimp_key_mapping[event.key]
        nearest_item = None
        min_distance = float('inf')
        for entity in entity_list:
            if isinstance(entity, Note) and not entity.disabled and entity.note == shrimp and not entity.is_sunk:
                distance = abs(self.player.pos.y - entity.height)
                if distance < min_distance:
                    min_distance = distance
                    nearest_item = entity
        # Performs a collision check
        if nearest_item and self.player.intersects_with(nearest_item.dimensions()):
            hit_sound = AssetManager.load_sound("drum-hitclap.mp3")
            hit_sound.play()
            nearest_item.remove()
            # Returns an event for increasing the score
            print(f"Collision detected with {nearest_item.note.name} shrimp!")
            return Event(INPUT_TIMING, success=True, score=1.0, player_id=self.player.id)

        if nearest_item is not None and not nearest_item.is_sunk:
            miss_sound = AssetManager.load_sound("soft-hitfinish.mp3")
            miss_sound.play()
            nearest_item.disabled = True
            return Event(INPUT_TIMING, success=False, score=1.0, player_id=self.player.id)

        return None
