from utils import *
from config import *
import pygame
import math
from bullet import Bullet





# making Player a child of the Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, bg_width, bg_height):  # CHANGED: Add bg_width and bg_height as arguments
        super().__init__()

        # VISUAL VARIABLES
        self.image = pygame.Surface(player_size)
        self.image.fill(cute_purple)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        # GAMEPLAY VARIABLES
        self.speed = 5
        self.health = 100
        self.bullet_cooldown = 0

        # NEW: Store background dimensions
        self.bg_width = bg_width
        self.bg_height = bg_height

    def update(self):
        keys = pygame.key.get_pressed()

        # CHANGED: Use bg_width and bg_height to restrict movement
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < self.bg_height:  # Use bg_height for bottom limit
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < self.bg_width:  # Use bg_width for right limit
            self.rect.x += self.speed

    def shoot(self, bullets):
        """
        bullets --> pygame group where I will add bullets
        """
        # cooldown ==> how many frames I need to wait until I can shoot again
        if self.bullet_cooldown <= 0:
            # === defining the directions in which the bullets will fly ===
            # these 4 directions are, in order, right, left, up, down
            for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:
                bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
                bullets.add(bullet)

            # resetting the cooldown
            self.bullet_cooldown = fps

        self.bullet_cooldown -= 1











