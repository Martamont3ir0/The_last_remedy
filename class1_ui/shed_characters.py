import pygame
import random
from config import *

class Coin(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect()

        # starting the coin at a random valid location on the screen
        self.rect.x = random.randint(0, 500)
        self.rect.y = random.randint(100, 530)

class Cactus(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/cactus.png')
        self.image = pygame.transform.scale(self.image, (40,80))
        self.rect = self.image.get_rect()

        # starting the cactus at a random valid location on the screen
        self.rect.x = random.randint(0, 500)
        self.rect.y = random.randint(100, 530)

class Monster(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/desert_monster.png')
        self.image = pygame.transform.scale(self.image, (400,200))
        self.rect = self.image.get_rect()

        # starting the monster at a precise location on the screen
        self.rect.x = 2000 #out of bounds but this way it will take longer to get to the player
        self.rect.y = 400

        self.speed = 0.51
        self.health = 200

    def update(self):

        # Move the monster to the left
        self.rect.x -= self.speed

    def distance(self):
        """

        :return: distance between the position of the monster and the player's area
        """


        return self.rect.x - 720


