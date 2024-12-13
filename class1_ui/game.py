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

        if pygame.time.get_ticks() - start_time >= 10000: #After 10 seconds, the loop of start message ends
            running = False



        # Update the display (if needed)
        pygame.display.flip()
        pygame.time.delay(30) #delay to reduce resource usage

    pygame.mixer.music.play(-1)  # Start playing  in a loop
    current_state = "main"  # Start in the main area

    while True:
        if current_state == "main":
            current_state = execute_game(player, selected_character, interface_callback)
        elif current_state == "shed":
            current_state = shed(player, selected_character, bg_width,True)





def execute_game(player: Player = None, character_image_path=None,interface_callback=None):
    # SETUP:

    # setting up the background:
    background = pygame.image.load("img/backroundscenario.jpg")
    bg_width, bg_height = background.get_size()  # **New Line: Get the original size of the background image**

    # Create the player with the selected character image
    if player is None:
        player = Player(bg_width, character_image_path)

    # using the clock to control the time frame.
    clock = pygame.time.Clock()

    # screen setup:
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("The Last Remedy")

    # CHANGED: Initialize the player if not already passed
    if player is None:
        player = Player(bg_width)  # Pass bg_width. bg_height is already defined in the function player.

    # setting up the player
    player_group = pygame.sprite.Group()
    player_group.add(player)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # before starting our main loop, setup the enemy cooldown variable
    enemy_cooldown = 0

    # **New Line: Scroll position for the background**: Track how much the background has moved
    bg_x = 0  # **New Line: Initial position of the background**

    # Max countdown time for the user to survive
    countdown_time = 60

    running = True
    start_time = time.time()
    while running:
        clock.tick(fps)

        # Handle events first
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Calculate remaining time
        elapsed_time = time.time() - start_time
        remaining_time = max(0, countdown_time - int(elapsed_time))

        # Check if the countdown has finished
        if remaining_time == 0:
            # Stop background music
            pygame.mixer.music.stop()
            puzzle_message(background,player,character_image_path,bg_width)


        #Clear the screen
        screen.fill((0, 0, 0))  # Fill with black or any color



        # **Changed Line: Move the background as the player moves to the right**
        bg_x -= player.speed

        # Reset background position for seamless looping
        if bg_x <= -bg_width:
            bg_x = 0

        # Draw the background
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + bg_width, 0))

        #Displaying player's info
        user_info(player, screen, False)

        # Render the countdown timer
        font = pygame.font.Font(None, 46)  # Adjust font size as needed
        timer_text = font.render(f"{remaining_time // 60}:{remaining_time % 60:02d}", True, deep_black)
        screen.blit(timer_text, (width // 2 - timer_text.get_width() // 2, 10))  # Centered at the top


        # Player shooting
        player.shoot(bullets)

        # Spawning enemies every two seconds
        if enemy_cooldown <= 0:
            enemy = Enemy()
            enemies.add(enemy)
            enemy_cooldown = fps * 2  # Reset cooldown

        enemy_cooldown -= 1

        # Update groups
        player_group.update()
        enemies.update(player)
        bullets.update()

        # Draw the player and enemies
        player_group.draw(screen)
        enemies.draw(screen)
        bullets.draw(screen)

        # Handle bullet collisions
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 10
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()

        # Handle enemy/player collisions
        collided_enemies = pygame.sprite.spritecollide(player, enemies, False)

        # Check if the player has collided with any enemies
        if collided_enemies:
            damage = 20#example of damage from enemy
            player.take_damage(damage,False)#making player's health influenced by this damage, depending whether or not they are invincible
            for drone in collided_enemies:
                drone.kill() #kill the enemy so it doesn't affect more the player
                print(player.health) #checking if health is being correctly messed with

        # Check if the player's health is less than or equal to zero, which means death time
        if player.health <= 0:
            death(interface_callback)
            player.health = 100



        # Check if the player has reached the right edge of the screen
        if player.rect.right >= width:
            # Stop background music
            pygame.mixer.music.stop()
            shed(player,character_image_path,bg_width,True)

        # Update the display once after all drawing is done
        pygame.display.flip()


