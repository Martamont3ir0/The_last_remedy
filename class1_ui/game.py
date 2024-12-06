from enemy import Enemy
from config import *
import math
import pygame
from player import Player
from shed import shed
from start_message import *

def character_selection_screen():
    # Screen setup
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Character Selection")

    # Load character images
    girl_image = pygame.image.load("img/lucaquinn_female.jpg")  # Correct image path for girl character
    boy_image = pygame.image.load("img/lucaquinn_male.jpg")  # Correct image path for boy character

    # Scale images
    girl_image = pygame.transform.scale(girl_image, (150, 150))
    boy_image = pygame.transform.scale(boy_image, (150, 150))

    # Positions
    girl_rect = girl_image.get_rect(center=(width // 3, height // 2))
    boy_rect = boy_image.get_rect(center=(2 * width // 3, height // 2))

    selected_character = None  # To store the choice
    character_image_path = None  # Store the selected image path
    clock = pygame.time.Clock()

    while selected_character is None:
        screen.fill((0, 0, 0))  # Clear screen with black background

        # Draw instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Choose your character", True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, height // 4))
        screen.blit(text, text_rect)

        # Draw character images
        screen.blit(girl_image, girl_rect)
        screen.blit(boy_image, boy_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if girl_rect.collidepoint(event.pos):
                    selected_character = "girl"  # Set to "girl"
                    character_image_path = "img/female-removebg-preview.png"  # Store the image path
                elif boy_rect.collidepoint(event.pos):
                    selected_character = "boy"  # Set to "boy"
                    character_image_path = "img/male-removebg-preview__1_-removebg-preview.png"  # Store the image path

        pygame.display.flip()
        clock.tick(30)

    return character_image_path  # Return the image path, not just the character name

def game_loop():
    # Character selection
    selected_character = character_selection_screen()  # Returns image path

    # Debugging: Check if image path was correctly selected
    print(f"Character image path: {selected_character}")  # Debugging output

    # Show start message after character selection
    level1_title = "Level 1: 'The Map'"
    level1_description = [
        "Objective: Find the map that reveals the location of Solanum in the Wastes.",
        "Key Challenge: Avoid being caught by the Sentinel Drones until the clock resets.",
        "Once it does, they’ll leave you alone, allowing you to search for the map.",
        "Note: GRAVITY DOESN’T EXIST IN THIS PLACE, so you’ll be floating as you navigate."
    ]
    # SETUP:
    # Load the background image and get its size (bg_width, bg_height)
    background = pygame.image.load("img/backroundscenario.jpg")  # Make sure this path is correct
    bg_width, bg_height = background.get_size()  # Get the dimensions of the background image

    screen = pygame.display.set_mode(resolution)
    show_start_message(screen,level1_title,level1_description,background)



    # Create the player with the selected image path, and pass bg_width and bg_height
    player = Player(bg_width, bg_height, selected_character)  # Pass image path directly

    current_state = "main"  # Start in the main area

    while True:
        if current_state == "main":
            current_state = execute_game(player, selected_character)
        elif current_state == "shed":
            current_state = shed(player, selected_character, bg_width, bg_height)





def execute_game(player: Player = None, character_image_path=None):
    # SETUP:

    # setting up the background:
    background = pygame.image.load("img/backroundscenario.jpg")
    bg_width, bg_height = background.get_size()  # **New Line: Get the original size of the background image**

    # Create the player with the selected character image
    if player is None:
        player = Player(bg_width, bg_height, character_image_path)

    # using the clock to control the time frame.
    clock = pygame.time.Clock()

    # screen setup:
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("The Last Remedy")

    # CHANGED: Initialize the player if not already passed
    if player is None:
        player = Player(bg_width, bg_height)  # Pass bg_width and bg_height

    # setting up the player
    player_group = pygame.sprite.Group()
    player_group.add(player)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # before starting our main loop, setup the enemy cooldown variable
    enemy_cooldown = 0

    # **New Line: Scroll position for the background**: Track how much the background has moved
    bg_x = 0  # **New Line: Initial position of the background**

    running = True
    while running:
        clock.tick(fps)

        screen.blit(background, (0, 0))

        # handling events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        player.shoot(bullets)

        # spawning enemies every two seconds
        if enemy_cooldown <= 0:
            enemy = Enemy()
            enemies.add(enemy)
            enemy_cooldown = fps * 2

        enemy_cooldown -= 1

        player_group.update()
        enemies.update(player)
        bullets.update()

        # **Changed Line: Move the background as the player moves to the right**
        bg_x -= player.speed

        if bg_x <= -bg_width:
            bg_x = 0  # **Changed Line: Reset background position to create seamless looping**

        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + bg_width, 0))

        player_group.draw(screen)
        enemies.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)

        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 5
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()

        if player.rect.right >= width:
            return "shed"
        pygame.display.flip()

    pygame.quit()


