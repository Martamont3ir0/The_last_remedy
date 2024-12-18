from enemy import Enemy
from config import *
import pygame
from player import Player
from shed import shed
from start_message import *
import time
from puzzle_message import *
from death import death
from user_info import *
from surprise_pup import Surprise

def character_selection_screen():
    # Screen setup
    screen = pygame.display.set_mode(resolution)

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

def game_loop(interface_callback):
    # Character selection
    selected_character = character_selection_screen()  # Returns image path

    # Debugging: Check if image path was correctly selected
    print(f"Character image path: {selected_character}")  # Debugging output

    # SETUP:
    # Load the background image and get its size (bg_width, bg_height)
    background = pygame.image.load("img/backroundscenario.jpg")  # Make sure this path is correct
    bg_width, bg_height = background.get_size()  # Get the dimensions of the background image

    # Create the player with the selected image path, and pass bg_width. bg_height is already defined in the function player.
    player = Player(bg_width, selected_character)  # Pass image path directly

    # Show start message after character selection
    level1_title = "Level 1: 'The Map'"
    level1_description = [
        "Objective: Find the map that reveals the location of Solanum in the Wastes.",
        "Key Challenge: Avoid being caught by the Sentinel Drones until the clock resets.",
        "Once it does, they’ll leave you alone, allowing you to search for the map.",
        "Note: GRAVITY DOESN’T EXIST IN THIS PLACE, so you’ll be floating as you navigate."
    ]

    #Stop background interface music
    pygame.mixer.music.stop()

    screen = pygame.display.set_mode(resolution)
    #Show level start message
    show_start_message(screen, level1_title, level1_description, background, player)


    # add city alarm music
    pygame.mixer.music.load("audio/city alarm.wav")
    # Set the volume (0.0 to 1.0)
    pygame.mixer.music.set_volume(0.1)  # Sets the volume to 10%

    # Start a timer
    start_time = pygame.time.get_ticks()

    # Main loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        if pygame.time.get_ticks() - start_time >= 1000: #After 10 seconds, the loop of start message ends
            running = False



        # Update the display (if needed)
        pygame.display.flip()
        pygame.time.delay(30) #delay to reduce resource usage

    pygame.mixer.music.play(-1)  # Start playing  in a loop
    current_state = "main"  # Start in the main area

    while True:
        if current_state == "main":
            current_state = execute_game(player, selected_character, interface_callback)
        elif current_state == "puzzle_message":
            current_state = puzzle_message(background, player, selected_character, bg_width)
        elif current_state == "puzzle_game":
            current_state = puzzle_game(screen, player, selected_character, bg_width)
        elif current_state == "shed_light":
            current_state = shed(player, selected_character, bg_width,True,False)
        elif current_state == "shed_normal":
            current_state = shed(player, selected_character, bg_width,False,False)
        elif current_state == "shed_map":
            current_state = shed(player, selected_character, bg_width, False, True)
        elif current_state == "backpack":
            current_state = backpack(screen, player, selected_character, bg_width)
        elif current_state == "shop":
            current_state = shop_window(screen, player, selected_character, bg_width)
        elif current_state == "death":
            current_state = death(interface_callback)


def execute_game(player: Player = None, character_image_path=None, interface_callback=None):
    # SETUP:

    # Setting up the background
    background = pygame.image.load("img/backroundscenario.jpg")
    bg_width, bg_height = background.get_size()

    # Create the player with the selected character image
    if player is None:
        player = Player(bg_width, character_image_path)

    # Screen setup
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("The Last Remedy")

    # Initialize groups
    player_group = pygame.sprite.Group()
    player_group.add(player)

    bullets = pygame.sprite.Group()
    lasers = pygame.sprite.Group()  # Group for lasers
    enemies = pygame.sprite.Group()

    surprise_count = 0
    enemy_cooldown = 0
    bg_x = 0

    #creating our level 1 powerup variables so that they can be examined later
    speed_boost = False
    shield = False
    surprise = pygame.sprite.Group()


    # Max countdown time for survival
    countdown_time = 10
    start_time = time.time()

    running = True
    while running:
        clock.tick(fps)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        # Calculate remaining time
        elapsed_time = time.time() - start_time
        remaining_time = max(0, countdown_time - int(elapsed_time))

        #at a certain time, the surprise balloon must appear
        if remaining_time == 45 and surprise_count == 0:
            surprise_ex = Surprise()  # Create a new surprise balloon
            surprise.add(surprise_ex)  # Add it to the group
            speed_boost = True  # Set to true so that the powerup is speed boost
            surprise_count += 1
            print("incoming surprise....")



        if remaining_time == 25 and surprise_count == 1:
            surprise_ex = Surprise()  # Create a new surprise balloon
            surprise.add(surprise_ex)  # Add it to the group
            shield = True  # Set to true so that the powerup is invincibility
            surprise_count += 1
            print("incoming surprise....")

        # Clear the screen
        screen.fill((0, 0, 0))


        # Check if the timer runs out
        if remaining_time == 0:
            pygame.mixer.music.stop()
            return "puzzle_message"

        # Clear the screen
        screen.fill((0, 0, 0))

        # Move background for parallax effect
        bg_x -= 5 #equal to player's speed in a normal situation
        if bg_x <= -bg_width:
            bg_x = 0
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + bg_width, 0))

        # Display player info
        user_info(player, screen, False)

        # Render countdown timer
        font = pygame.font.Font(None, 46)
        timer_text = font.render(f"{remaining_time // 10}:{remaining_time % 10:02d}", True, deep_black)
        screen.blit(timer_text, (width // 2 - timer_text.get_width() // 2, 10))

        # Player shooting (bullets and lasers)
        keys = pygame.key.get_pressed()
        player.shoot(bullets, lasers)  # Pass keys to handle laser shooting

        # Spawn enemies
        if enemy_cooldown <= 0:
            enemy = Enemy()
            enemies.add(enemy)
            enemy_cooldown = fps * 2  # Cooldown reset
        enemy_cooldown -= 1

        # Update all groups
        player_group.update()
        bullets.update()
        lasers.update(player)
        enemies.update(player)


        # Draw everything
        player_group.draw(screen)
        enemies.draw(screen)
        bullets.draw(screen)
        lasers.draw(screen)

        # Draw the surprise balloon if the flag is set
        surprise.update()  # Update the surprise balloon
        surprise.draw(screen)  # Draw the surprise balloon

        # Bullet collisions
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 10
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()

        # Laser collisions
        for laser in lasers:
            collided_enemies = pygame.sprite.spritecollide(laser, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 30  # Lasers deal more damage
                if enemy.health <= 0:
                    enemy.kill()

        # Handle player collisions with enemies
        collided_enemies = pygame.sprite.spritecollide(player, enemies, False)
        if collided_enemies:
            player.take_damage(10, player.is_invincible)
            for drone in collided_enemies:
                drone.kill()

        # Initialize powerup to None
        powerup = None

        # Check whether the surprise offers invincibility or speed boost
        if shield and pygame.sprite.spritecollide(player, surprise, True):
            powerup = Invincibility(15)  # Create a variable with the powerup
            shield = False


        if speed_boost and pygame.sprite.spritecollide(player, surprise, True):
            powerup = SpeedBoost(20)  # Create a variable with the powerup
            speed_boost = False

        # Handle applying the powerup
        if powerup is not None:
            powerup.apply(player)


        # Check player health
        if player.health <= 0:
            player.health = 100
            return "death"


        # Check if the player reaches the right edge
        if player.rect.right >= width:
            pygame.mixer.music.stop()
            return "shed_light"

        pygame.display.flip()