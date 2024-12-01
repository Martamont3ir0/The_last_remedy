from enemy import Enemy
from config import *
import math
import pygame
from player import Player
from shed import shed

def game_loop():
    # Setup
    player = None  # Initialize player as None
    current_state = "main"  # Start in the main area

    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)



def execute_game(player: Player = None):

    # SETUP:

    # setting up the background:
    background = pygame.image.load("img/backroundscenario.jpg")
    bg_width, bg_height = background.get_size()  # **New Line: Get the original size of the background image**


    # using the clock to control the time frame.
    clock = pygame.time.Clock()

    # screen setup:
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")

    # CHANGED: Initialize the player if not already passed
    if player is None:
        player = Player(bg_width, bg_height)  # Pass bg_width and bg_height


    # setting up the player
    # creating an empty group for the player
    player_group = pygame.sprite.Group()

    # adding the player to the group
    player_group.add(player)

    # creating an empty bullet group that will be given as input to the player.shoot() method
    bullets = pygame.sprite.Group()

    # creating the enemy group
    enemies = pygame.sprite.Group()

    # before starting our main loop, setup the enemy cooldown variable
    enemy_cooldown = 0

    # **New Line: Scroll position for the background**: Track how much the background has moved
    bg_x = 0  # **New Line: Initial position of the background**

    # MAIN GAME LOOP

    running = True

    while running:

        # controlling the frame rate
        clock.tick(fps)

        # setting up the background
        screen.blit(background, (0, 0))

        # handling events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # automatically shoot bullets from the player
        player.shoot(bullets)

        # spawning enemies every two seconds
        if enemy_cooldown <= 0:
            # creating an enemy...would be so cool if there were more than one type... oh well...
            enemy = Enemy()

            # adding the enemy to the group
            enemies.add(enemy)

            # in bullets, we use fps to spawn every second. Here we double that, to spawn every two seconds
            enemy_cooldown = fps * 2

        # updating the enemy cooldown
        enemy_cooldown -= 1

        # updating positions and visuals:
        # calling the .update() method of all the instances in the player group
        player_group.update()

        # updating the bullets and enemy groups
        enemies.update(player)
        bullets.update()

        # **Changed Line: Move the background as the player moves to the right**
        bg_x -= player.speed  # **Changed Line: Shift the background left based on player speed**

        # **Changed Line: Wrap the background when it moves off-screen**
        if bg_x <= -bg_width:
            bg_x = 0  # **Changed Line: Reset background position to create seamless looping**

        # **Changed Line: Draw the background (twice to create the scrolling effect)**
        screen.blit(background, (bg_x, 0))  # **Changed Line: First background at bg_x position**
        screen.blit(background, (bg_x + bg_width, 0))  # **Changed Line: Second background right after the first**

        # drawing the player and enemies sprites on the screen
        player_group.draw(screen)
        enemies.draw(screen)

        # drawing the bullet sprites:
        for bullet in bullets:
            bullet.draw(screen)

        # checking for collisions between player bullets and enemies
        for bullet in bullets:
            # getting the enemies that were hit by a bullet
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)

            for enemy in collided_enemies:

                # every hit enemy needs to lose life
                # every bullet hit will reduce the life by 5 hp
                enemy.health -= 5

                # removing the bullet from the screen (as it's lodged in the enemy's heart)
                bullet.kill()

                # checking if the enemy is ripperino
                if enemy.health <= 0:
                    enemy.kill()

        if player.rect.right >= width:
            return "shed"  # Transition to the shed area
        pygame.display.flip()

    # the main while game loop has terminated and the game ends
    pygame.quit()





