"""
Bullet module for Mayhem Clone.

Contains the Bullet sprite class, which represents a projectile
fired by a spaceship.
"""

import pygame
import config


class Bullet(pygame.sprite.Sprite):
    """
    A projectile fired by a spaceship.

    Moves in a straight line and disappears after a fixed lifetime.
    """

    def __init__(self, pos, direction, owner_id):
        """
        Initialise the bullet.
        """
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.vel = direction * config.BULLET_SPEED
        self.owner = owner_id
        self.lifetime = config.BULLET_LIFETIME

        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(self.image, config.YELLOW, (3, 3), 3)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def update(self, *args, **kwargs):
        """Move the bullet forward and count down its lifetime."""
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
