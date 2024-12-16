import pygame
from config import *

class Laser(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        """
        Laser class similar to bullets class.
        Objective: redner continuous beams.
        parameters:
        -x: start x position
        -y: start y position
        -direction: direction that laser moves
        -color: laser color (default color is red)
        -length: length of the laser beam
        """
        super().__init__()
        self.color = (255, 0, 0)  # Red laser
        self.glow_color= (255,50,50)
        self.length = 400
        self.width = 4  # Laser thickness
        self.glow_width= 10


        # Create a surface for the laser
        self.image = pygame.Surface((self.length, self.glow_width), pygame.SRCALPHA)
        self.rect = self.image.get_rect(midleft=(player_rect.centerx, player_rect.centery))
        self.create_laser()

    def create_laser(self):
        """
        Draw the laser with glow and gradient effect.
        """
        # Draw the glow (larger and transparent)
        pygame.draw.line(self.image, self.glow_color, (0, self.glow_width // 2), (self.length, self.glow_width // 2), self.glow_width)

        # Draw the core laser line (smaller and solid)
        pygame.draw.line(self.image, self.color, (0, self.glow_width // 2), (self.length, self.glow_width // 2), self.width)

    def update(self, player):
        """
        Update the laser's position to match the player's position.
        """
        self.rect.midleft = (player.rect.centerx, player.rect.centery)