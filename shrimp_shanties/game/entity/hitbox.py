from pygame import Rect

from shrimp_shanties.game.entity import Entity


class Hitbox(Entity):
    def dimensions(self) -> Rect:
        pass

    def intersects_with(self, other: Rect) -> bool:
        """ Returns whether given rectangle intersects with self """
        return self.dimensions().colliderect(other)

    def intersects_with_all(self, others: list[Rect]) -> int | None:
        """ Returns the index of the intersecting rectangle in the given list or None """
        i = self.dimensions().collidelist(others)
        return i if i != -1 else None
