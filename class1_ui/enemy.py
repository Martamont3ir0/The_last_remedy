from config import *
import pygame
import random
import math
from PIL import Image

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/animated_drone_with_no_background-removebg-preview.png')
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()

        # starting the enemy at a random valid location on the screen
        self.rect.x = random.randint(0, width - enemy_size[0])
        self.rect.y = random.randint(0, height - enemy_size[-1])

        # setting a random initial speed for the enemy booo maybe different enemy types would be cool
        self.speed = random.randint(1, 3)
        # setting the healthbar
        self.health = 10

    def update(self, player):

        """
        receiving the player as input so that we can assure the enemies move in the players' direction

        """

        # determining the direction (in radians) of the movement based on the player location
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        # getting the direction in radians
        direction = math.atan2(dy, dx)

        # moving the enemy towards the player --> like bullet
        self.rect.x += self.speed * math.cos(direction)
        self.rect.y += self.speed * math.sin(direction)

        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)