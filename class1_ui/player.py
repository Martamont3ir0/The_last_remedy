from utils import *
from config import *
import math
import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize a Player instance
        """
        super().__init__()
        #drawing variables
        self.image=pygame.Surface(player_size)
        self.image.fill(blue)
        self.rect= self.image.get_rect()
        self.rect.center= (width//2, height//2)

        #gameplay variables
        self.speed= 5 #multipler for how fast things move
        self.health= 100
        self.bullet_cooldown= 0


    def update(self):
        """
        Update the position of the player based on keyboard input 
        """

        keys= pygame.key.get_pressed()
        #moving upwards
        if keys[pygame.K_w] and self.rect.top>0:
            self.rect.y -= self.speed
            #its removing because if you are moving upwards you are reducing
        #moving downwards
        if keys[pygame.K_s] and self.rect.bottom<height:
            self.rect.y += self.speed
        #moving left
        if keys[pygame.K_a] and self.rect.left>0:
            self.rect.x -= self.speed
        #moving right
        if keys[pygame.K_d] and self.rect.right<width:
            self.rect.x += self.speed

    def shoot(self,bullets:pygame.sprite.Group):
        """
        Shoot bullets in 4 direction depending on cooldown

        Args
        ----
        bullets (pygame.sprite.Group):
            The bullet group that we will add the new ones to
        """
        #if you are shooting
        if self.bullet_cooldown<=0:
            for angle in [0, math.pi/2, math.pi,3*math.pi/2]:
                bullet=Bullet(
                    self.rect.center[0], self.rect.center[1], angle
                )
                bullets.add(bullet)
            self.bullet_cooldown= fps  #Frames until the next shot
        #if you are not
        self.bullet_cooldown-=1









