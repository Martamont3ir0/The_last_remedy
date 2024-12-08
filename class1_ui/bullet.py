from config import *
import pygame
import math


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):

        super().__init__()

        # setting base attributes
        self.direction = direction
        self.radius = bullet_size
        self.color = deep_black
        self.speed = 7

        # Create a surface for the bullet
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)  # Create a transparent surface
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius),self.radius)  # Draw the bullet on the surface
        self.rect = self.image.get_rect(center=(x, y))  # Set the initial position of the bullet

    def update(self):

        # updating the bullet's position based on the speed and the direction
        # (x, y) --> (cos, sin)
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

        # killing the bullet if it goes off-screen.
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.kill()

