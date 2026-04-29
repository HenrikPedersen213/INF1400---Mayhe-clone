"""
Spaceship module for Mayhem Clone.

Contains the Spaceship sprite class, which handles player input,
physics (thrust, gravity, rotation), fuel management, and firing.
"""

import math
import pygame
import config


class Spaceship(pygame.sprite.Sprite):
    """
    A player-controlled spaceship.

    Handles rotation, thrust, gravity, fuel, firing, and collision response.
    """

    _fire_cooldown = {}  # class-level dict keyed by player_id

    def __init__(self, x, y, color, controls, player_id):
        """
        Initialise the spaceship.

        """
        super().__init__()
        self.color = color
        self.controls = controls
        self.player_id = player_id

        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.angle = 0.0  # degrees; 0 = pointing up

        self.fuel = config.STARTING_FUEL
        self.score = 0
        self.alive = True

        self.base_image = self._build_surface()
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def _build_surface(self):
        """
        Create the base (unrotated) ship surface as a triangle.

        """
        size = 30
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        tip   = (size // 2, 2)
        left  = (2, size - 2)
        right = (size - 2, size - 2)
        pygame.draw.polygon(surf, self.color, [tip, left, right])
        pygame.draw.polygon(surf, config.WHITE, [tip, left, right], 1)
        return surf

    def _rotate_image(self):
        """Rotate the base image to match the current angle and update self.rect."""
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def _key(self, name):
        """
        Convert a key name string to a pygame key constant.
        """
        mapping = {
            "left":  pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "up":    pygame.K_UP,
            "down":  pygame.K_DOWN,
            "space": pygame.K_SPACE,
            "rctrl": pygame.K_RCTRL,
            "lctrl": pygame.K_LCTRL,
        }
        if name in mapping:
            return mapping[name]
        return getattr(pygame, "K_" + name, pygame.K_SPACE)

    