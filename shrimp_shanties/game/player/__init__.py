import pygame
from pygame import Rect, Surface
from pygame.event import Event

from shrimp_shanties import WIDTH, HEIGHT
from shrimp_shanties.asset_manager import AssetManager
from shrimp_shanties.game.entity.hitbox import Hitbox
from shrimp_shanties.game.next_id import next_event_id


PLAYER_HIT_SPACE = next_event_id()


class Player(Hitbox):
    def __init__(self, id=0):
        super().__init__(id)
        self.sprite = AssetManager.load_texture("front-background.png")
        self.scale_hitbox()

    def scale_hitbox(self):
        # Gets the current window dimensions.
        window_width, window_height = pygame.display.get_surface().get_size()

        # Calculates the scaled dimensions for the hitbox.
        hitbox_width = window_width
        hitbox_height = window_height // 5
        hitbox_left = 0
        hitbox_top = window_height * 4 // 5

        # Updates the hitbox position and size.
        self.pos = Rect(hitbox_left, hitbox_top, hitbox_width, hitbox_height)

        # Scales the sprite to match the dimensions.
        self.sprite = pygame.transform.scale(self.sprite, (hitbox_width, hitbox_height))

    def dimensions(self) -> Rect:
        return self.pos

    def draw(self, screen: Surface):
        screen.blit(self.sprite, self.pos)

    def register_for_events(self, em):
        em.register_event(self, pygame.KEYDOWN)
        em.register_event(self, pygame.VIDEORESIZE)  # Detects window resize.

    def handle_event(self, event):
        import shrimp_shanties.game.entity_manager as em

        match event.type:
            case pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    event = Event(PLAYER_HIT_SPACE, player_id=self.id)
                    pygame.event.post(event)
            case pygame.VIDEORESIZE:
                self.scale_hitbox()  # Updates the hitbox when the window is resized.
            case em.PROCESS_TURN:
                pass
