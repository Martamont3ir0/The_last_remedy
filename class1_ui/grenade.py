import pygame
import math


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        """
        Initialize the Grenade object. Set its initial position, image, and target position.
        Calculate the velocity needed for the grenade to reach its target within a given time.

        :param x: The x-coordinate where the grenade is initially placed.
        :param y: The y-coordinate where the grenade is initially placed.
        :param target_pos: The target position (x, y) the grenade should move toward.
        """
        super().__init__()

        self.target_pos = target_pos  # The target position for the grenade to reach
        self.image = pygame.image.load('img/grenade.png')  # Load grenade image
        self.image = pygame.transform.scale(self.image, (30, 50))  # Resize the grenade image
        self.rect = self.image.get_rect(center=(x, y))  # Set the initial position of the grenade

        self.time = 0  # Initialize time that will track how long the grenade has been in motion
        self.max_time = 1.5  # Maximum time to reach the target
        self.start_position = (x, y)  # Starting position of the grenade
        self.velocity = self.calculate_initial_velocity()  # Calculate the initial velocity needed to reach the target

    def calculate_initial_velocity(self):
        """
        Calculate the initial velocities for the grenade to reach the target position in the specified time.

        :return: A tuple containing the horizontal and vertical velocities.
        """
        # Calculate the difference between the target and starting positions
        dx = self.target_pos[0] - self.start_position[0]
        dy = self.target_pos[1] - self.start_position[1]

        # Calculate the initial horizontal and vertical velocities
        vel_x = dx / self.max_time  # Horizontal velocity
        vel_y = dy / self.max_time  # Vertical velocity

        return (vel_x, vel_y)

    def update(self, player):
        """
        Update the grenade's position over time, moving it toward the target.
        After reaching the target, the grenade is removed and the player's weapon is reset.

        :param player: The player object to update the weapon status after grenade reach.
        """
        # Increment the time to simulate the grenade's motion
        self.time += 0.05  # Controls the speed of the grenade's movement

        # Ensure that the grenade doesn't move past the target position
        if self.time > self.max_time:
            self.time = self.max_time  # Stop updating once the maximum time is reached

        # Calculate the new position based on the initial velocity and time
        vel_x = self.velocity[0]  # Get horizontal velocity
        vel_y = self.velocity[1]  # Get vertical velocity

        # Update the grenade's position based on its velocity and elapsed time
        self.rect.x = int(self.start_position[0] + vel_x * self.time)  # Update horizontal position
        self.rect.y = int(self.start_position[1] + vel_y * self.time)  # Update vertical position

        # If the grenade has reached its target, remove it and reset the player's weapon
        if self.time >= self.max_time:
            player.weapon = "None"  # Reset the player's weapon to "None"
            self.kill()  # Remove the grenade from all sprite groups
