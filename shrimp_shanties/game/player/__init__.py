import pygame
from pygame import Rect, Surface
from pygame.event import Event

from shrimp_shanties import WIDTH, HEIGHT, AssetManager
from shrimp_shanties.game.entity.hitbox import Hitbox


PLAYER_HIT_SPACE = pygame.USEREVENT + 1


class Player(Hitbox):
    def __init__(self, id=0):
        super().__init__(id)
        # Rect(left, top, width, height)
        self.pos = Rect(WIDTH / 2 - 100, HEIGHT / 2 - 100, 200, 200)
        self.sprite = AssetManager.load_texture("shrimp.png")
        self.sprite = pygame.transform.scale(self.sprite, (200, 200))

    def dimensions(self) -> Rect:
        return self.pos

    def draw(self, screen: Surface):
        screen.blit(self.sprite, self.pos)

    def register_for_events(self, em):
        em.register_event(self, pygame.KEYDOWN)

    def handle_event(self, event):
        match event.type:
            case pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("sending event")
                    event = Event(PLAYER_HIT_SPACE, player_id=self.id)
                    pygame.event.post(event)
                    pass
