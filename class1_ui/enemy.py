from config import *
import pygame
import random
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the Enemy object. Set up its image, position, speed, health, and spawn frequency.
        The enemy is placed at a random location on the screen, and its speed is set randomly.
        """
        super().__init__()

        # Load and resize the enemy image
        self.image = pygame.image.load('img/animated_drone_with_no_background-removebg-preview.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        # Start the enemy at a random valid location on the screen
        self.rect.x = random.randint(0, width - enemy_size[0])  # Ensure it fits within the screen width
        self.rect.y = random.randint(0, 551)  # Random position along the y-axis (vertical)

        # Set a random speed for the enemy between 1 and 3
        self.speed = random.randint(1, 3)

        # Set the initial health of the enemy
        self.health = 10

        # Set the frequency at which the enemy spawns (for future use)
        self.spawn_frequency = 1

    def update(self, player):
        """
        Update the position of the enemy based on the player's position.
        The enemy moves towards the player by calculating the direction vector and using trigonometry.

        :param player: The player object that the enemy will move towards
        """
        # Determine the direction (in radians) of movement based on the player's location
        dx = player.rect.x - self.rect.x  # Difference in x position
        dy = player.rect.y - self.rect.y  # Difference in y position

        # Calculate the angle (in radians) to the player
        direction = math.atan2(dy, dx)

        # Move the enemy towards the player (like a homing bullet)
        self.rect.x += self.speed * math.cos(direction)  # Update the x position
        self.rect.y += self.speed * math.sin(direction)  # Update the y position

        # Ensure the position values are integers (avoids subpixel movement)
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
