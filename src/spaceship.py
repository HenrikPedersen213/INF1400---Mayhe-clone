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

    def update(self, dt, bullet_group, all_sprites):
        """
        Update physics, handle input, and fire bullets.

        Args:
            dt (float): Delta-time in seconds (for frame-rate independence).
            bullet_group (pygame.sprite.Group): Group to add new bullets into.
            all_sprites (pygame.sprite.Group): Master group for new sprites.
        """
        if not self.alive:
            return

        keys = pygame.key.get_pressed()

        # Rotation
        if keys[self._key(self.controls["left"])]:
            self.angle -= config.ROTATION_SPEED
        if keys[self._key(self.controls["right"])]:
            self.angle += config.ROTATION_SPEED

        # Thrust
        thrusting = keys[self._key(self.controls["thrust"])] and self.fuel > 0
        if thrusting:
            rad = math.radians(self.angle)
            thrust_vec = pygame.math.Vector2(math.sin(rad), -math.cos(rad))
            self.vel += thrust_vec * config.THRUST_POWER
            self.fuel -= config.FUEL_BURN_RATE

        # Space like movement with air ressistance
        # Yeah... make it make sense
        self.vel = self.vel * config.GRAVITY


        # Speed cap
        if self.vel.length() > config.MAX_SPEED:
            self.vel.scale_to_length(config.MAX_SPEED)

        # Position (Euler integration)
        self.pos += self.vel

        # Screen wrapping
        self.pos.x %= config.SCREEN_WIDTH
        self.pos.y %= config.SCREEN_HEIGHT

        # Fire
        if keys[self._key(self.controls["fire"])]:
            self._try_fire(bullet_group, all_sprites)

        self._rotate_image()

    def _try_fire(self, bullet_group, all_sprites):
        """
        Spawn a bullet if cooldown has expired and bullet limit allows.

        """
        from bullet import Bullet  # local import avoids circular dependency

        own = [b for b in bullet_group if b.owner == self.player_id]
        if len(own) >= config.MAX_BULLETS:
            return

        now = pygame.time.get_ticks()
        last = Spaceship._fire_cooldown.get(self.player_id, 0)
        if now - last < 300:
            return
        Spaceship._fire_cooldown[self.player_id] = now

        rad = math.radians(self.angle)
        direction = pygame.math.Vector2(math.sin(rad), -math.cos(rad))
        spawn = self.pos + direction * 18
        bullet = Bullet(spawn, direction, self.player_id)
        bullet_group.add(bullet)
        all_sprites.add(bullet)

    def crash(self):
        """Handle a crash: deduct score and respawn the ship."""
        self.score = max(0, self.score - config.SCORE_CRASH_PENALTY)
        self._respawn()

    def _respawn(self):
        """Reset position, velocity, and fuel to starting values."""
        start_positions = {1: (config.SCREEN_WIDTH/4, 100), 2: ((config.SCREEN_WIDTH/4)*3, 100)}
        x, y = start_positions.get(self.player_id, (400, 100))
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.angle = 0.0
        self.fuel = config.STARTING_FUEL

    def refuel(self):
        """Add fuel when the ship is resting on a landing pad."""
        self.fuel = min(config.STARTING_FUEL, self.fuel + config.REFUEL_RATE)