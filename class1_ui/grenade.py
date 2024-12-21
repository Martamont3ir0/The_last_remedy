import pygame
import math


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        super().__init__()

        self.target_pos = target_pos
        self.image = pygame.image.load('img/grenade.png')
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect(center=(x, y))  # Set the initial position of the grenade

        self.time = 0
        self.max_time = 1.5  # Time to reach the target
        self.start_position = (x, y)
        self.velocity = self.calculate_initial_velocity()

    def calculate_initial_velocity(self):
        # Calculate the distance to the target
        dx = self.target_pos[0] - self.start_position[0]
        dy = self.target_pos[1] - self.start_position[1]

        # Calculate the initial horizontal and vertical velocities
        vel_x = dx / self.max_time  # Horizontal velocity
        vel_y = dy / self.max_time  # Vertical velocity

        return (vel_x, vel_y)

    def update(self, player):
        # Increment time for the grenade's motion
        self.time += 0.05  # Control the speed of the throw
        if self.time > self.max_time:
            self.time = self.max_time  # Stop updating after reaching the target

        # Calculate the new position
        vel_x = self.velocity[0]  # Horizontal velocity
        vel_y = self.velocity[1]  # Vertical velocity

        # Update the position based on time and velocity
        self.rect.x = int(self.start_position[0] + vel_x * self.time)  # Horizontal position
        self.rect.y = int(self.start_position[1] + vel_y * self.time)  # Vertical position

        # Remove grenade after thrown
        if self.time >= self.max_time:
            player.weapon = "None"  # Set player's weapon to None
            self.kill()  # Remove the grenade from all groups