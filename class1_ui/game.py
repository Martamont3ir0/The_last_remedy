from config import *
import math
import pygame

from enemy import Enemy
from player import Player

def execute_game():
    """
     Main function to execute the game loop
    """
    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # setting up the background:
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("img/grass.jpg")
    background = pygame.transform.scale(background, (width, height))

    # Player setup
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Initialize the bullet group
    bullets = pygame.sprite.Group()

    # Initialize the enemy group
    enemies = pygame.sprite.Group()
    enemy_spawn_timer = 0

    running = True
    while running:
        # Control frame rate
        clock.tick(fps)
        # Fill the background
        screen.blit(background, (0, 0))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Shooting
        player.shoot(bullets)

        # Spawning the enemies
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            enemy_spawn_timer = 2 * fps # Every two seconds

        # Checking for collisions between enemies and bullets
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 5  # Decrease health by 5, for example
                bullet.kill()  # Destroy the bullet
                if enemy.health <= 0:
                    enemy.kill()  # Destroy the enemy

        # Update the enemy spawn timer
        enemy_spawn_timer -= 1

        # Update positions
        player_group.update()
        bullets.update()
        enemies.update(player)


        # Drawing the objects
        player_group.draw(screen)
        enemies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        pygame.display.flip()
