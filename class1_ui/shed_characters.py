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
        self.rect.y = random.randint(100, 515)
        self.is_alive = True

        # Convert the coin's state to a dictionary for saving
    def to_dict(self):
        return {
            'x': self.rect.x,
            'y': self.rect.y,
            'is_alive': self.is_alive
        }

    # Create a coin instance from a dictionary (for loading)
    @classmethod
    def from_dict(cls, data):
        coin = cls()
        coin.rect.x = data['x']
        coin.rect.y = data['y']
        coin.is_alive = data['is_alive']
        return coin

class Cactus(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/cactus.png')
        self.image = pygame.transform.scale(self.image, (40,80))
        self.rect = self.image.get_rect()

        # starting the cactus at a random valid location on the screen
        self.rect.x = random.randint(0, 500)
        self.rect.y = random.randint(100, 515)
        self.is_alive = True

    # Convert the cactus's state to a dictionary for saving
    def to_dict(self):
        return {
            'x': self.rect.x,
            'y': self.rect.y,
            'is_alive': self.is_alive
        }

    # Create a cactus instance from a dictionary (for loading)
    @classmethod
    def from_dict(cls, data):
        cactus = cls()
        cactus.rect.x = data['x']
        cactus.rect.y = data['y']
        cactus.is_alive = data['is_alive']
        return cactus

class Monster(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/desert_monster.png')
        self.image = pygame.transform.scale(self.image, (400,200))
        self.rect = self.image.get_rect()

        # starting the monster at a precise location on the screen
        self.rect.x = 1500 #out of bounds but this way it will take longer to get to the player
        self.rect.y = 400

        self.speed = 0.51
        self.is_alive = True

    def update(self,stop_pos):

        if self.is_alive:
            if self.rect.x > stop_pos[0]:
                # Move the monster to the left
                self.rect.x -= self.speed
            elif self.rect.x < stop_pos[0]:
                self.rect.x = stop_pos[0]  # Snap to stop position if overshot

    def kill_monster(self, stop_pos):
            self.is_alive = False  # Set the monster as not alive
            if stop_pos[0] < 600: #making sure the solanum will appear completely on the screen
                self.rect.x = stop_pos[0]  # Set the monster's position to the stop position
            else:
                self.rect.x = 600

    def distance(self):
        """

        :return: distance between the position of the monster and the player's area
        """

        return self.rect.x - 720

    # Convert the monster's state to a dictionary for saving
    def to_dict(self):
        return {
            'x': self.rect.x,
            'y': self.rect.y,
            'is_alive': self.is_alive
        }

    # Create a monster instance from a dictionary (for loading)
    @classmethod
    def from_dict(cls, data):
        monster = cls()
        monster.rect.x = data['x']
        monster.rect.y = data['y']
        monster.is_alive = data['is_alive']
        return monster

