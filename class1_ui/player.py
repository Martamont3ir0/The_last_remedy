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
    def __init__(self,health, money, state, character,type):
        super().__init__()

        # VISUAL VARIABLES
        self.selected_character = type
        self.character_image_path = character
        self.image = pygame.image.load(self.character_image_path)
        self.image = pygame.transform.scale(self.image, (55, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.shake_counter = 0  # Counter for shake duration
        # Shadow attributes
        self.shadow_color = (0, 0, 0, 0)  # transparent shadow
        self.shadow_offset = (0, 10)  # Offset for the shadow position
        self.shadow_size = (self.rect.width, self.rect.height)  # Size of the shadow
        self.shadow_surface = pygame.Surface(self.shadow_size, pygame.SRCALPHA)  # Create a surface with alpha
        self.update_shadow()  # Initialize shadow surface

        # GAMEPLAY VARIABLES
        self.speed = 5
        self.health = health
        self.bullet_cooldown = 0
        self.is_invincible = False
        self.money = money
        self.weapon = "Default Bullets"
        self.pup = None
        self.level = None
        self.state = state

        # NEW: Store background dimensions
        self.bg_width = 720
        self.bg_height = 550

        #laser attributes
        self.laser_mode= False #default: bullets enabled
        self.laser_cooldown =0 #cooldown timer for lasers

        #backpack items handling
        self.map_used = False  # to check if map was used and characters can be seen
        self.glasses_used = False  # to check if glasses were used and light can be turned off

        #level 2 handles
        self.seen_message2 = False
        self.shed_characters = {}
        self.default_list = [] #for powerups and functions on levels it cant be applied enemies group

        #level 3 handles
        self.feelings = "Happy"
        self.seen_message3 = False

    def update_shadow(self):
        # Update shadow surface and position
        self.shadow_surface.fill(self.shadow_color)  # Fill with shadow color
        self.shadow_rect = self.shadow_surface.get_rect(topleft=(self.rect.x + self.shadow_offset[0], self.rect.y + self.shadow_offset[1]))


    def set_character(self,character, image_path):
        """
        Set the character image and update the sprite image.
        :param character: selected character chosen
        :param image_path: image_path that the character should take
        """
        self.character_image_path = image_path
        self.selected_character = character
        self.image = pygame.image.load(self.character_image_path)  # Load the new image
        self.image = pygame.transform.scale(self.image, (55, 100))
        self.rect = self.image.get_rect(center=self.rect.center)  # Keep the same position


    def take_damage(self,damage,is_invincible):
        if not is_invincible:
            self.health -= damage
        else:
            return self.health




    def update(self,level):
        """

        :return:
        """
        keys = pygame.key.get_pressed()

        if level == 1:

            if keys[pygame.K_w] and self.rect.top > 0:
                self.rect.y -= self.speed
                #self.shake() #Calling the shake function each time it moves
            if keys[pygame.K_s] and self.rect.bottom < 551:  # Use bg_height for bottom limit
                self.rect.y += self.speed
                #self.shake()

        elif level == 2:

            if keys[pygame.K_w] and self.rect.top > 140:
                self.rect.y -= self.speed
                #self.shake() #Calling the shake function each time it moves
            if keys[pygame.K_s] and self.rect.bottom < 551:  # Use bg_height for bottom limit
                self.rect.y += self.speed
                #self.shake()


        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.shake()
        if keys[pygame.K_d] and self.rect.right < 720:  # Use bg_width for right limit
            self.rect.x += self.speed
            self.shake()

        # Handle shaking effect
        if self.shake_counter > 0:
            self.rect.x += random.randint(-shake_intensity, shake_intensity)
            self.rect.y += random.randint(-shake_intensity, shake_intensity)
            self.shake_counter -= 1  # Decrease the shake counter

        self.update_shadow()  # Update shadow position based on player position

    def shake(self):
        """
        Shaking implementation so that the player looks more realistic when moving
        :return: initiation of shake counter
        """
        if self.shake_counter == 0:  # Start shaking if not already shaking
            self.shake_counter = shake_duration

    def shoot(self, bullets, lasers):
        """
        Handles shooting for bullets and lasers.
        -spacebar fires a continuous laser
        -bullets are fired in all directions with a cooldown
        """
        keys = pygame.key.get_pressed()

        # BULLET SHOOTING - Left Mouse Button
        if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
            if self.bullet_cooldown <= 0:
                # Fire bullets in all directions
                for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:
                    bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
                    bullets.add(bullet)
                self.bullet_cooldown = fps//8  # Reset cooldown


        # LASER SHOOTING - SPACE key
        if keys[pygame.K_SPACE] and self.weapon == "Laser" and self.use_laser:
            # Ensure only one laser exists at a time
            if not lasers:
                laser = Laser(self.rect)
                lasers.add(laser)
        else:
            # Stop the laser when SPACE key is released
            lasers.empty()

        if self.bullet_cooldown>0:
            self.bullet_cooldown-=1

