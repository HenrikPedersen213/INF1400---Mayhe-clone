"""
Game module for Mayhem Clone.

Contains the HUD display helper and the main Game class, which owns
the game loop, sprite groups, input handling, collision detection,
and rendering.

Run this file directly to start the game.
"""

import pygame
import config
from spaceship import Spaceship
from bullet import Bullet
from obstacles import Obstacle, LandingPad


class HUD:
    """
    Heads-up display showing scores and fuel bars for both players.

    Not a sprite — drawn directly onto the screen each frame.
    """

    def __init__(self, font):
        """
        Initialise the HUD.
        """
        self.font = font

    def draw(self, screen, ship1, ship2):
        """
        Draw score and fuel information for both players.

        """
        self._draw_player_info(screen, ship1, 10, config.BLUE)
        self._draw_player_info(screen, ship2, config.SCREEN_WIDTH - 160, config.RED)

    def _draw_player_info(self, screen, ship, x, color):
        """
        Render one player's score label and fuel bar.

        """
        label = self.font.render(f"P{ship.player_id}  Score: {ship.score}", True, color)
        screen.blit(label, (x, 8))

        bar_w = 150
        pygame.draw.rect(screen, config.DARK_GREY, (x, 30, bar_w, 10))
        fill = int(bar_w * ship.fuel / config.STARTING_FUEL)
        pygame.draw.rect(screen, color, (x, 30, fill, 10))
        pygame.draw.rect(screen, config.WHITE, (x, 30, bar_w, 10), 1)


class Game:
    """
    Top-level game object that owns the main loop, sprite groups, and logic.

    Instantiate once and call run() to start the game.
    """

    def __init__(self):
        """Initialise pygame, the window, all sprites, and sprite groups."""
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 16)
        self.running = True

        # Sprite groups
        self.all_sprites  = pygame.sprite.Group()
        self.ships        = pygame.sprite.Group()
        self.bullets      = pygame.sprite.Group()
        self.obstacles    = pygame.sprite.Group()
        self.landing_pads = pygame.sprite.Group()

        self._setup_world()
        self.hud = HUD(self.font)

    def _setup_world(self):
        """Create and register all sprites for the initial game world."""
        p1_controls = {"left": config.P1_LEFT, "right": config.P1_RIGHT, "thrust": config.P1_THRUST,  "fire": config.P1_FIRE}
        p2_controls = {"left": config.P2_LEFT,    "right": config.P2_RIGHT,     "thrust": config.P2_THRUST,   "fire": config.P2_FIRE}

        self.ship1 = Spaceship(config.SCREEN_WIDTH/4, 100, config.BLUE, p1_controls, 1)
        self.ship2 = Spaceship((config.SCREEN_WIDTH/4)*3, 100, config.RED,  p2_controls, 2)
        for ship in (self.ship1, self.ship2):
            self.ships.add(ship)
            self.all_sprites.add(ship)

        for i in range(0,5):
            obs = Obstacle(200*2.3*i, 250*i, 100, 300)
            self.obstacles.add(obs)
            self.all_sprites.add(obs)
        
        for i in range(0,5):
            obs = Obstacle((200*2.3*i), 700- 250*i, 100, 300)
            self.obstacles.add(obs)
            self.all_sprites.add(obs)

        floor = Obstacle(0, config.SCREEN_HEIGHT - 20, config.SCREEN_WIDTH, 20, config.GREY)
        self.obstacles.add(floor)
        self.all_sprites.add(floor)
        
        roof = Obstacle(0, 0, config.SCREEN_WIDTH, 20, config.GREY)
        self.obstacles.add(roof)
        self.all_sprites.add(roof)

        pad1 = LandingPad(config.SCREEN_WIDTH/4*0.8,  config.SCREEN_HEIGHT-400,50,50)
        pad2 = LandingPad(config.SCREEN_WIDTH/4*3, config.SCREEN_HEIGHT-400,50,50)
        for pad in (pad1, pad2):
            self.landing_pads.add(pad)
            self.all_sprites.add(pad)


    def run(self):
        """
        Main loop
        Run the game loop until the window is closed or ESC is pressed.
        """
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0  # seconds
            self._handle_events()
            self._update(dt)
            self._check_collisions()
            self._draw()

        pygame.quit()


    def _handle_events(self):
        """Process pygame events such as window close and ESC key."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def _update(self, dt):
        """
        Update all sprites for one frame.

        """
        for ship in self.ships:
            ship.update(dt, self.bullets, self.all_sprites)

        self.bullets.update()
      


    def _check_collisions(self):
        """Check all relevant collisions and apply gameplay effects."""
        # Bullets absorbed by obstacles
        pygame.sprite.groupcollide(self.bullets, self.obstacles, True, False)

        # Bullets hit ships
        for ship in self.ships:
            hits = pygame.sprite.spritecollide(ship, self.bullets, True)
            for bullet in hits:
                if bullet.owner != ship.player_id:
                    shooter = self.ship1 if bullet.owner == 1 else self.ship2
                    shooter.score += config.SCORE_KILL
                    ship.crash()

        # Ships hit obstacles
        for ship in self.ships:
            if pygame.sprite.spritecollideany(ship, self.obstacles):
                if ship.vel.length() > 0.1:
                    ship.crash()
                else:
                    ship.vel.y = 0
                    ship.vel.x *= 0.8

        # Ships on landing pads — refuel
        for ship in self.ships:
            if pygame.sprite.spritecollideany(ship, self.landing_pads):
                ship.refuel()

        # Ships collide with each other
        if pygame.sprite.collide_rect(self.ship1, self.ship2):
            if (self.ship1.vel - self.ship2.vel).length() > 1.0:
                self.ship1.crash()
                self.ship2.crash()


    def _draw(self):
        """Clear the screen, draw all sprites, overlay the HUD, and flip."""
        self.screen.fill(config.BLACK)
        self.all_sprites.draw(self.screen)
        self.hud.draw(self.screen, self.ship1, self.ship2)
        pygame.display.flip()


if __name__ == "__main__":
    Game().run()