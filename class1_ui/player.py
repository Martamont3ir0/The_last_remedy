from utils import *
from config import *
import pygame
import math
from bullet import Bullet
from PIL import Image
import random
from laser import Laser
import json

#Constants for my shaking implementation
shake_duration = 10  # Number of frames to shake
shake_intensity = 1  # Maximum pixels to shake

# making Player a child of the Sprite class
class Player(pygame.sprite.Sprite):
    """
    A class representing the player in the game.

    This class defines the player's attributes, including visual properties (like character image and shadow),
    gameplay-related variables (like health, speed, and money), and the player's actions (like taking damage).

    Attributes:
        selected_character (str): Type of the character selected.
        character_image_path (str): Path to the character's image.
        image (pygame.Surface): The image representing the player.
        rect (pygame.Rect): The rectangle that defines the player's position and size.
        shadow_color (tuple): RGBA values for the player's shadow color.
        shadow_offset (tuple): The offset for the shadow's position relative to the player.
        shadow_size (tuple): The size of the shadow surface.
        shadow_surface (pygame.Surface): The surface that holds the shadow.
        speed (int): The player's movement speed.
        health (int): The player's health.
        bullet_cooldown (int): The cooldown for the player's weapon.
        is_invincible (bool): Whether the player is invincible or not.
        money (int): The player's current amount of money.
        weapon (str): The type of weapon the player is using.
        pup (Any): Placeholder for any power-up object the player might have.
        level (Any): The player's current level.
        state (str): The player's state in the game.
        bg_width (int): Background width for level display.
        bg_height (int): Background height for level display.
        laser_mode (bool): Whether the player is using a laser weapon.
        laser_cooldown (int): The cooldown timer for the laser weapon.
        map_used (bool): Whether the map has been used in the game.
        glasses_used (bool): Whether the glasses have been used to manipulate light.
        seen_message2 (bool): Whether a specific message in level 2 has been seen.
        shed_characters (dict): Dictionary to store characters in level 2.
        default_list (list): A list for default power-ups or enemy functions in level 2.
        feelings (str): The player's emotional state, used in level 3.
        seen_message3 (bool): Whether a specific message in level 3 has been seen.
    """

    def __init__(self, health, money, state, character, type):
        """
        Initialize a Player object with specified attributes.

        :param health: Initial health of the player.
        :param money: Initial amount of money the player has.
        :param state: Initial state of the player in the game.
        :param character: The selected character's name.
        :param type: Type of the character selected (e.g., 'Girl', 'Boy').
        """
        super().__init__()

        # VISUAL VARIABLES
        self.selected_character = type
        self.character_image_path = character
        self.image = pygame.image.load(self.character_image_path)  # Load character image
        self.image = pygame.transform.scale(self.image, (55, 100))  # Scale to proper size
        self.rect = self.image.get_rect()  # Get the rectangle for the image
        self.rect.center = (width // 2, height // 2)  # Place the character at the center
        self.shake_counter = 0  # Counter for shake duration

        # Shadow attributes
        self.shadow_color = (0, 0, 0, 0)  # Transparent shadow by default
        self.shadow_offset = (0, 10)  # Shadow position offset
        self.shadow_size = (self.rect.width, self.rect.height)  # Shadow size
        self.shadow_surface = pygame.Surface(self.shadow_size, pygame.SRCALPHA)  # Surface for shadow with alpha transparency
        self.update_shadow()  # Initialize the shadow surface

        # GAMEPLAY VARIABLES
        self.speed = 5  # Player movement speed
        self.health = health  # Player's initial health
        self.bullet_cooldown = 0  # Cooldown for shooting bullets
        self.is_invincible = False  # Initially, player is not invincible
        self.money = money  # Player's starting money
        self.weapon = "Default Bullets"  # Default weapon
        self.pup = None  # Placeholder for power-ups
        self.level = None  # Placeholder for the player's current level
        self.state = state  # Current state of the player in the game

        # NEW: Store background dimensions
        self.bg_width = 720  # Width of the background
        self.bg_height = 550  # Height of the background

        # Laser weapon attributes
        self.laser_mode = False  # Laser mode is off by default
        self.laser_cooldown = 0  # Laser cooldown timer

        # Backpack items handling
        self.map_used = False  # Track if the map was used
        self.glasses_used = False  # Track if the glasses were used to turn off lights

        # Level 2 handling
        self.seen_message2 = False  # Whether a message in level 2 has been seen
        self.shed_characters = {}  # Characters in level 2
        self.default_list = []  # Default power-ups and enemies list for level 2

        # Level 3 handling
        self.feelings = "Happy"  # Default feelings state in level 3
        self.seen_message3 = False  # Whether a message in level 3 has been seen

    def update_shadow(self):
        """
        Update the shadow's surface and position.

        This method updates the shadow's appearance based on the player's position.
        """
        self.shadow_surface.fill(self.shadow_color)  # Fill the shadow surface with the shadow color
        self.shadow_rect = self.shadow_surface.get_rect(topleft=(self.rect.x + self.shadow_offset[0], self.rect.y + self.shadow_offset[1]))  # Set the shadow's position

    def set_character(self, character, image_path):
        """
        Set the character image and update the sprite image.

        This method allows switching the player's character and updating the visual representation.

        :param character: Name of the selected character.
        :param image_path: Path to the image file representing the new character.
        """
        self.character_image_path = image_path  # Set new character image path
        self.selected_character = character  # Update the character type
        self.image = pygame.image.load(self.character_image_path)  # Load the new image
        self.image = pygame.transform.scale(self.image, (55, 100))  # Scale the image to the appropriate size
        self.rect = self.image.get_rect(center=self.rect.center)  # Maintain the current position of the player

    def take_damage(self, damage, is_invincible):
        """
        Reduce the player's health by a specified amount of damage.

        The player's health will only decrease if they are not invincible.

        :param damage: The amount of damage to be taken.
        :param is_invincible: Whether the player is currently invincible (if true, damage is not applied).
        :return: The player's health after taking damage (or the same health if invincible).
        """
        if not is_invincible:
            self.health -= damage  # Reduce health if not invincible
        return self.health  # Return the current health

    def update(self, level):
        """
        Update the player's position based on keyboard inputs and the current level.

        This method checks for movement keys (W, A, S, D) and moves the player accordingly,
        while also handling any necessary screen boundaries and level-specific restrictions.
        Additionally, the shake effect is triggered when the player moves.

        :param level: The current level of the game. Determines the boundaries for the player's movement.
        :return: None
        """
        keys = pygame.key.get_pressed()  # Get the current state of all keys

        # Movement for level 1
        if level == 1:
            if keys[pygame.K_w] and self.rect.top > 0:  # Move up
                self.rect.y -= self.speed
                # self.shake()  # Optionally call shake function when moving
            if keys[pygame.K_s] and self.rect.bottom < 551:  # Move down (using bg_height)
                self.rect.y += self.speed
                # self.shake()  # Optionally call shake function when moving

        # Movement for level 2
        elif level == 2:
            if keys[pygame.K_w] and self.rect.top > 140:  # Level 2 has different movement boundary
                self.rect.y -= self.speed
                # self.shake()  # Optionally call shake function when moving
            if keys[pygame.K_s] and self.rect.bottom < 551:  # Move down (using bg_height)
                self.rect.y += self.speed
                # self.shake()  # Optionally call shake function when moving

        # Movement for left and right (common to both levels)
        if keys[pygame.K_a] and self.rect.left > 0:  # Move left
            self.rect.x -= self.speed
            self.shake()  # Trigger shake effect when moving
        if keys[pygame.K_d] and self.rect.right < 720:  # Move right (using bg_width)
            self.rect.x += self.speed
            self.shake()  # Trigger shake effect when moving

        # Handle shaking effect (applies a random shake offset)
        if self.shake_counter > 0:
            self.rect.x += random.randint(-shake_intensity, shake_intensity)  # Random shake in X
            self.rect.y += random.randint(-shake_intensity, shake_intensity)  # Random shake in Y
            self.shake_counter -= 1  # Decrease the shake counter

        self.update_shadow()  # Update the shadow's position based on the player's new position

    def shake(self):
        """
        Initiates the shaking effect when the player moves.

        This method sets the shake counter to a specified duration, triggering
        a random shake of the player's position.

        :return: None
        """
        if self.shake_counter == 0:  # Start shaking if not already shaking
            self.shake_counter = shake_duration  # Set the shake duration

    def shoot(self, bullets, lasers):
        """
        Handles the shooting mechanism for both bullets and lasers.

        - Left mouse button fires bullets in all directions with a cooldown between shots.
        - Spacebar fires a continuous laser if the laser weapon is equipped.
        - The laser is fired in a single direction and only one laser can exist at a time.

        :param bullets: A sprite group where the newly created bullets are added.
        :param lasers: A sprite group where the laser is added when fired.
        :return: None
        """
        keys = pygame.key.get_pressed()  # Get the current state of all keys

        # BULLET SHOOTING - Left Mouse Button
        if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
            if self.bullet_cooldown <= 0:  # Ensure the bullet is not on cooldown
                # Fire bullets in four directions (0°, 180°, 90°, and 270°)
                for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:
                    bullet = Bullet(self.rect.centerx, self.rect.centery, angle)  # Create bullet object
                    bullets.add(bullet)  # Add the bullet to the bullets sprite group
                self.bullet_cooldown = fps // 8  # Reset the cooldown (8th of a second)

        # LASER SHOOTING - SPACE key
        if keys[pygame.K_SPACE] and self.weapon == "Laser" and self.use_laser:  # Check for laser weapon and activation
            # Ensure only one laser exists at a time
            if not lasers:
                laser = Laser(self.rect)  # Create a laser at the player's current position
                lasers.add(laser)  # Add the laser to the lasers sprite group
        else:
            lasers.empty()  # Remove the laser if the spacebar is released

        # Reduce cooldown timer if necessary
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1  # Decrease the bullet cooldown counter


