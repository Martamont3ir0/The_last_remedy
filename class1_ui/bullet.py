from config import *
import pygame
import math


class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet that is fired from a player's weapon or an enemy's weapon.

    The bullet moves in a specified direction at a constant speed and disappears when it goes off-screen.

    Attributes:
        direction (float): The angle at which the bullet is traveling (in radians).
        radius (int): The size of the bullet (its radius).
        color (tuple): The color of the bullet (represented as RGB values).
        speed (int): The speed at which the bullet moves.
        image (pygame.Surface): The surface representing the bullet.
        rect (pygame.Rect): The rectangle used to detect collision and track the bullet's position.
    """

    def __init__(self, x, y, direction):
        """
        Initializes a new Bullet instance.

        Args:
            x (int): The starting x-coordinate of the bullet.
            y (int): The starting y-coordinate of the bullet.
            direction (float): The angle in radians at which the bullet will move.
        """
        super().__init__()

        # Setting basic attributes
        self.direction = direction  # Direction in radians
        self.radius = bullet_size  # The size of the bullet (radius)
        self.color = deep_black  # Color of the bullet
        self.speed = 7  # Speed of the bullet

        # Create a surface for the bullet
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)  # Transparent surface
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)  # Draw the bullet
        self.rect = self.image.get_rect(center=(x, y))  # Set initial position of the bullet

    def update(self):
        """
        Updates the position of the bullet based on its speed and direction.

        The bullet moves in the direction specified during initialization. If the bullet goes off-screen,
        it is removed from the game.

        This method is typically called every frame to update the bullet's position.
        """
        # Update the bullet's position based on its speed and direction
        self.rect.x += int(self.speed * math.cos(self.direction))  # Update the x-coordinate
        self.rect.y += int(self.speed * math.sin(self.direction))  # Update the y-coordinate

        # Check if the bullet is off-screen (out of bounds), and if so, remove it
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > 551:
            self.kill()  # Remove the bullet from all sprite groups
