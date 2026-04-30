"""
Obstacles module for Mayhem Clone.

Contains the Obstacle and LandingPad sprite classes, which represent
static objects in the game world.
"""

import pygame
import config


class Obstacle(pygame.sprite.Sprite):
    """
    A static rectangular obstacle that absorbs bullets and destroys ships on impact.
    """

    def __init__(self, x, y, width, height, color=None):
        """
        Initialise the obstacle.

        """
        super().__init__()
        color = color or config.GREY
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, *args, **kwargs):
        """Static sprite — nothing to update."""
        pass


class LandingPad(pygame.sprite.Sprite):
    """
    A landing pad where a spaceship can land and refuel.

    The Game class checks for collisions with this sprite and calls
    ship.refuel() when the ship is moving slowly enough.
    """

    def __init__(self, x, y, width=80, height=10):
        """
        Initialise the landing pad.

        """
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(config.GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))