import random
from enum import Enum

import pygame
from pygame import Surface, Rect
from pygame.event import post, Event

from shrimp_shanties import AssetManager
from shrimp_shanties.game.entity.hitbox import Hitbox
from shrimp_shanties.game.entity_manager import PROCESS_TURN
from shrimp_shanties.game.next_id import next_entity_id


class Shrimp(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2
    BLUE = 3


class Note(Hitbox):
    def __init__(self, note: Shrimp):
        super().__init__(next_entity_id())
        self.note = note
        self.height_ratio = 0.0
        self.x_ratio = (70 + 250 * self.note.value) / 1000
        file_name = f"{note.name.lower()}shrimp.png"
        self.original_sprite = AssetManager.load_texture(file_name)
        self.sprite = self.original_sprite
        self.sprite = pygame.transform.rotate(self.sprite, -90 * random.randint(0, 3))
        self.height = 0
        self.disabled = False
        self.is_sunk = False
        self.scale_sprite()  # Scales the sprite to window size when spawning.

    def register_for_events(self, em):
        em.register_event(self, pygame.VIDEORESIZE)

    def draw(self, screen: Surface):
        screen_width, screen_height = screen.get_size()
        x = int(self.x_ratio * screen_width)
        y = int(self.height_ratio * screen_height)
        sprite = self.sprite.copy()
        if self.disabled:
            overlay_color = pygame.Color(0, 0, 0).lerp((255, 255, 255), 0.625)
            width, height = self.sprite.get_size()
            scale_factor = 1
            new_width = width / scale_factor
            new_height = height / scale_factor
            scaled_size = (new_width, new_height)
            coloured = pygame.Surface(scaled_size, pygame.SRCALPHA)
            coloured.fill(overlay_color)
            sprite.blit(coloured, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        if self.is_sunk and self.disabled:
            overlay_color = pygame.Color(255, 255, 255).lerp((3, 68, 171), 1)
            coloured = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
            coloured.fill(overlay_color)
            sprite.blit(coloured, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        elif self.is_sunk:
            overlay_color = pygame.Color(0, 0, 0).lerp((3, 68, 171), 1)
            coloured = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
            coloured.fill(overlay_color)
            sprite.blit(coloured, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(sprite, Rect(x, y, sprite.get_width(), sprite.get_height()))

    def handle_event(self, event):
        if event.type == PROCESS_TURN:
            # multiply speed by delta in seconds to run at 60 fps
            self.height_ratio += 0.01 * event.delta * 60
            if self.height_ratio > 0.62 and not self.is_sunk:
                if not self.disabled:
                    sunk_sound = AssetManager.load_sound("combobreak.mp3")
                    sunk_sound.set_volume(0.5)
                    sunk_sound.play()
                self.is_sunk = True
                if not self.disabled:
                    from shrimp_shanties.game.check.input_timing import INPUT_TIMING
                    post(Event(INPUT_TIMING, success=False))
            if self.height_ratio > 1.0:
                self.remove()
        elif event.type == pygame.VIDEORESIZE:
            self.scale_sprite()  # Scales the spawned sprites when the window is resized.

    def dimensions(self) -> Rect:
        screen_width, screen_height = pygame.display.get_surface().get_size()
        x = int(self.x_ratio * screen_width)
        y = int(self.height_ratio * screen_height)
        return Rect(x, y, self.sprite.get_width(), self.sprite.get_height())

    def scale_sprite(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        scale_factor = min(screen_width * 4 / 1000, screen_height * 4 / 600)
        new_width = int(self.original_sprite.get_width() * scale_factor)
        new_height = int(self.original_sprite.get_height() * scale_factor)
        self.sprite = pygame.transform.scale(self.original_sprite, (new_width, new_height))

    def __str__(self):
        return f"Note(dir={self.note} disabled={self.disabled} sunk={self.is_sunk})"
