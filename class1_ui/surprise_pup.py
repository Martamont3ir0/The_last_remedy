import pygame
import random
from config import *


class Surprise(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/surprise.png')
        self.image = pygame.transform.scale(self.image, (80,130))
        self.rect = self.image.get_rect()

        # starting the balloon at a random valid location on the screen
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = 0

        self.speed = 1


    def update(self):

        # Move the surprise down
        self.rect.y += self.speed
        # Remove the surprise if it goes off the screen
        if self.rect.y > 550:
            self.kill()  # Remove the sprite from all groups

