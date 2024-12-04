from utils import *
from config import *
import pygame
import math
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, bg_width, bg_height, character_image_path):
        super().__init__()

        if character_image_path:
            self.image = pygame.image.load(character_image_path)
            self.image = pygame.transform.scale(self.image, (50, 50))
        else:  # Placeholder image
            self.image = pygame.Surface((50, 50))
            self.image.fill(cute_purple)

        self.rect = self.image.get_rect()
        self.rect.center = (bg_width // 2, bg_height // 2)

        # Gameplay variables
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.bullet_cooldown = 0

        # Store background dimensions
        self.bg_width = bg_width
        self.bg_height = bg_height

        # Power-up variables
        self.power_up = None
        self.power_up_timer = 0

        # Animation variables
        self.frames = []  # Store animation frames
        self.current_frame = 0
        self.animation_speed = 0.2

    def update(self):
        keys = pygame.key.get_pressed()

        # Restrict movement within screen boundaries
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < self.bg_height:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < self.bg_width:
            self.rect.x += self.speed

        # Update power-up effects and animations
        self.update_power_up()
        self.update_animation()

    def shoot(self, bullets, target=None):
        if self.bullet_cooldown <= 0:
            if target:
                dx = target[0] - self.rect.centerx
                dy = target[1] - self.rect.centery
                angle = math.atan2(dy, dx)
            else:
                angle = 0  # Default shooting direction

            bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
            bullets.add(bullet)
            self.bullet_cooldown = 20

        self.bullet_cooldown -= 1

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Player dies if health is zero
        print(f"Health: {self.health}/{self.max_health}")

    def draw_health_bar(self, screen):
        health_ratio = self.health / self.max_health
        bar_width = 50
        bar_height = 5
        health_bar = pygame.Rect(self.rect.left, self.rect.top - 10, bar_width * health_ratio, bar_height)
        outline_bar = pygame.Rect(self.rect.left, self.rect.top - 10, bar_width, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), health_bar)  # Red for health
        pygame.draw.rect(screen, (255, 255, 255), outline_bar, 1)

    def apply_power_up(self, power_up_type, duration):
        self.power_up = power_up_type
        self.power_up_timer = duration

        if power_up_type == 'speed':
            self.speed *= 2
        elif power_up_type == 'health':
            self.health = min(self.max_health, self.health + 20)

    def update_power_up(self):
        if self.power_up_timer > 0:
            self.power_up_timer -= 1
        else:
            if self.power_up == 'speed':
                self.speed = 5  # Reset speed
            self.power_up = None

    def load_animation_frames(self, sprite_sheet_path, frame_width, frame_height):
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        for i in range(sprite_sheet.get_width() // frame_width):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            self.frames.append(frame)

    def update_animation(self):
        if not self.frames:  # Skip animation if no frames are loaded
            return

        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0  # Loop animation
        self.image = self.frames[int(self.current_frame)]
