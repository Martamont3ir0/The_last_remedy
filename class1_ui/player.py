from utils import *
from config import *
import pygame
import math
from bullet import Bullet
from PIL import Image
import random

#Constants for my shaking implementation
shake_duration = 10  # Number of frames to shake
shake_intensity = 5  # Maximum pixels to shake

# making Player a child of the Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, bg_width,character_image_path):
        super().__init__()

        # VISUAL VARIABLES
        self.image = pygame.image.load(character_image_path)
        self.image = pygame.transform.scale(self.image, (55, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.shake_counter = 0  # Counter for shake duration

        # GAMEPLAY VARIABLES
        self.speed = 5
        self.health = 100
        self.bullet_cooldown = 0
        self.is_invincible = False


        # NEW: Store background dimensions
        self.bg_width = bg_width
        self.bg_height = 551

    def take_damage(self,damage,is_invincible):
        if not is_invincible:
            self.health -= damage
        else:
            return self.health




    def update(self):
        """

        :return:
        """
        keys = pygame.key.get_pressed()

        # CHANGED: Use bg_width and bg_height to restrict movement
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
            self.shake() #Calling the shake function each time it moves
        if keys[pygame.K_s] and self.rect.bottom < self.bg_height:  # Use bg_height for bottom limit
            self.rect.y += self.speed
            self.shake()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.shake()
        if keys[pygame.K_d] and self.rect.right < self.bg_width:  # Use bg_width for right limit
            self.rect.x += self.speed
            self.shake()

        # Handle shaking effect
        if self.shake_counter > 0:
            self.rect.x += random.randint(-shake_intensity, shake_intensity)
            self.rect.y += random.randint(-shake_intensity, shake_intensity)
            self.shake_counter -= 1  # Decrease the shake counter

    def shake(self):
        """
        Shaking implementation so that the player looks more realistic when moving
        :return: initiation of shake counter
        """
        if self.shake_counter == 0:  # Start shaking if not already shaking
            self.shake_counter = shake_duration

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




