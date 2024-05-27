import pygame
from pygame import Rect, Surface
from pygame.event import Event

from shrimp_shanties.asset_manager import AssetManager
from shrimp_shanties.game.entity.hitbox import Hitbox
from shrimp_shanties.game.next_id import next_event_id

INPUT_TIMING = next_event_id()

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
        hitbox_height = window_height * 0.33333
        hitbox_left = 0
        hitbox_top = window_height * 0.66666

        # Updates the hitbox position and size.
        self.sprite_dims = Rect(hitbox_left, hitbox_top, hitbox_width, hitbox_height)
        self.pos = Rect(0., window_height * 0.66666, window_width, 20)

        # Scales the sprite to match the dimensions.
        self.sprite = pygame.transform.scale(self.sprite, (hitbox_width, hitbox_height))

    def dimensions(self) -> Rect:
        return self.pos

    def draw(self, screen: Surface):
        screen.blit(self.sprite, self.sprite_dims)
        pygame.draw.rect(screen, (255, 255, 255), self.pos)

    def register_for_events(self, em):
        em.register_event(self, pygame.KEYDOWN)
        em.register_event(self, pygame.VIDEORESIZE)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:  # Red Shrimp Note
                shrimp_event = Event(INPUT_TIMING, player_id=self.id, shrimp="RED")
                pygame.event.post(shrimp_event)
            elif event.key == pygame.K_s:  # Yellow Shrimp Note
                shrimp_event = Event(INPUT_TIMING, player_id=self.id, shrimp="YELLOW")
                pygame.event.post(shrimp_event)
            elif event.key == pygame.K_d:  # Green Shrimp Note
                shrimp_event = Event(INPUT_TIMING, player_id=self.id, shrimp="GREEN")
                pygame.event.post(shrimp_event)
            elif event.key == pygame.K_f:  # Blue Shrimp Note
                shrimp_event = Event(INPUT_TIMING, player_id=self.id, shrimp="BLUE")
                pygame.event.post(shrimp_event)
        elif event.type == pygame.VIDEORESIZE:
            self.scale_hitbox()  # Updates the hitbox when the window is resized.
