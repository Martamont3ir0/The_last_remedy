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
from level3 import *
from backpack import *
from utils import *

def character_selection_screen():
    # Screen setup
    screen = pygame.display.set_mode(resolution)



    # Load character images
    girl_image = pygame.image.load("img/lucaquinn_female.jpg")  # Correct image path for girl character
    boy_image = pygame.image.load("img/lucaquinn_male.jpg")  # Correct image path for boy character

    # Scale images
    girl_image = pygame.transform.scale(girl_image, (170, 170))
    boy_image = pygame.transform.scale(boy_image, (170, 170))

    # Positions
    girl_rect = girl_image.get_rect(center=(width // 3, 240))
    boy_rect = boy_image.get_rect(center=(2 * width // 3, 240))

    selected_character = None  # To store the choice
    character_image_path = None  # Store the selected image path
    clock = pygame.time.Clock()

    while selected_character is None:
        screen.fill((0, 0, 0))  # Clear screen with black background

        # Draw instructions
        font = pygame.font.Font(None, 36)
        text = font.render("CHOOSE YOUR CHARACTER", True, white)
        text_rect = text.get_rect(center=(width // 2, 80))
        screen.blit(text, text_rect)

        # Draw character images
        screen.blit(girl_image, girl_rect)
        screen.blit(boy_image, boy_rect)

        #Instruction panel
        font2 = pygame.font.Font(None, 26)
        title_movement = font.render("Player Movement", True, greenish)
        text_movement = font2.render("PRESS A to go left, PRESS D to go right, PRESS W to go up, PRESS S to go down", True, glowing_light_red)
        title_weapons = font.render("Weapons Handling", True, greenish)
        text_bullet = font2.render("For Bullets PRESS MOUSE LEFT BUTTON(various directions)", True, glowing_light_red)
        text_laser = font2.render("For Laser PRESS SPACE BAR", True, glowing_light_red)
        text_grenade = font2.render("Grenade PRESS MOUSE LEFT BUTTON on desired target(one shot for each grenade)", True, glowing_light_red)

        screen.blit(title_movement,title_movement.get_rect(center=(width // 2, 400)))
        screen.blit(text_movement, text_movement.get_rect(center=(width // 2, 450)))
        screen.blit(title_weapons, title_weapons.get_rect(center=(width // 2, 500)))
        screen.blit(text_bullet, text_bullet.get_rect(center=(width // 2, 550)))
        screen.blit(text_laser, text_laser.get_rect(center=(width // 2, 600)))
        screen.blit(text_grenade, text_grenade.get_rect(center=(width // 2, 650)))

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



        # Apply brightness and sound settings dynamically
        apply_brightness_and_sound(screen)

        pygame.display.flip()
        clock.tick(30)

    return selected_character,character_image_path  # Return the image path, not just the character name

def game_loop(interface_callback,player,current_state):
    # Character selection
    selected_character,character_image_path = character_selection_screen()  # Returns image path

    # SETUP:
    # Load the background image
    background = pygame.image.load("img/backroundscenario.jpg")  # Make sure this path is correct


    # Create the player with the selected image path

    player.set_character(selected_character,character_image_path)
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


    while True:
        player.current_state = current_state
        print(player.current_state)
        if current_state == "main":
            player.level = 1
            current_state = execute_game(player, interface_callback)
        elif current_state == "puzzle_message":
            current_state = puzzle_message(background, player)
        elif current_state == "puzzle_game":
            current_state = puzzle_game(screen)
        elif current_state == "shed":
            player.level = 2
            current_state = shed(player)
        elif current_state == "backpack":
            current_state = backpack(screen, player,player.level)
        elif current_state == "shop":
            current_state = shop_window(screen, player)
        elif current_state == "death":
            current_state = death(interface_callback,player)
        elif current_state == "level3":
            player.level = 3
            current_state = run_level3(screen,player)

        # applying brightness and sound settings in each loop iteration
        apply_brightness_and_sound(screen)
        pygame.display.flip()


def execute_game(player, interface_callback=None):
    # SETUP:

    # Setting up the background
    background = pygame.image.load("img/backroundscenario.jpg")

    player.level = 1
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
    de_spawner = False
    surprise = pygame.sprite.Group()


    # Max countdown time for survival
    countdown_time = 60
    start_time = time.time()
    start_time_pup = 3000000 #so it doesn't stop before the collision
    running = True
    pup_count =  0

    # Initialize powerup to None
    powerup = None
    while running:
        clock.tick(fps)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        key = pygame.key.get_pressed()
        # 'P' logic for saving
        if key[pygame.K_p]:
            save_game(player, player.state)

        # Calculate remaining time
        elapsed_time = time.time() - start_time
        remaining_time = max(0, countdown_time - int(elapsed_time))

        #at a certain time, the surprise balloon must appear
        if remaining_time == 48 and surprise_count == 0:
            surprise_ex = Surprise()  # Create a new surprise balloon
            surprise.add(surprise_ex)  # Add it to the group
            speed_boost = True  # Set to true so that the powerup is speed boost
            surprise_count += 1

            print("incoming surprise....")

        if remaining_time == 35 and surprise_count == 1:
            surprise_ex = Surprise()  # Create a new surprise balloon
            surprise.add(surprise_ex)  # Add it to the group
            shield = True  # Set to true so that the powerup is invincibility
            surprise_count += 1
            print("incoming surprise....")

        if remaining_time == 20 and surprise_count == 2:
            surprise_ex = Surprise()  # Create a new surprise balloon
            surprise.add(surprise_ex)  # Add it to the group
            de_spawner = True  # Set to true so that the powerup is de-spawner
            surprise_count += 1
            print("incoming surprise....")

        # Clear the screen
        screen.fill((0, 0, 0))


        # Check if the timer runs out
        if remaining_time == 0:
            pygame.mixer.music.stop()
            return "puzzle_message"


        # Move background for parallax effect
        bg_x -= 5 #equal to player's speed in a normal situation
        if bg_x <= -player.bg_width:
            bg_x = 0
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + player.bg_width, 0))

        # Display player info
        user_info(player, screen, False)

        # Render countdown timer
        font = pygame.font.Font(None, 46)
        timer_text = font.render(f"{remaining_time // 60}:{remaining_time % 60:02d}", True, deep_black)
        screen.blit(timer_text, (width // 2 - timer_text.get_width() // 2, 10))

        # Player shooting (bullets and lasers)
        keys = pygame.key.get_pressed()
        player.shoot(bullets, lasers)  # Pass keys to handle laser shooting

        # Spawn enemies
        if enemy_cooldown <= 0:
            enemy = Enemy()
            enemies.add(enemy)
            enemy_cooldown = fps * enemy.spawn_frequency  # Cooldown reset
        enemy_cooldown -= 1

        # Update all groups
        player_group.update(level=1)
        bullets.update()
        enemies.update(player)

        screen.blit(player.shadow_surface, player.shadow_rect)  # Draw invisible shadow

        # Draw everything
        player_group.draw(screen)
        enemies.draw(screen)
        bullets.draw(screen)


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


        # Handle player collisions with enemies
        collided_enemies = pygame.sprite.spritecollide(player, enemies, False)
        if collided_enemies:
            player.take_damage(10, player.is_invincible)
            for drone in collided_enemies:
                drone.kill()

        # Check whether the surprise offers invincibility, speed boost or de-spawner
        if speed_boost:
            powerup = SpeedBoost(10)# Create a variable with the powerup
            speed_boost = False
        if shield:
            powerup = Invincibility(10)  # Create a variable with the powerup
            shield = False
        if de_spawner:
            powerup = DeSpawner(10)
            de_spawner = False

        if powerup is not None:
            # Check for collision with surprise
            if pygame.sprite.spritecollide(player, surprise, True):
                powerup.affect_player(player,enemies)  # Apply the power-up
                # Only apply the power-up if it hasn't been used yet
                if pup_count == 0:
                    pup_count +=1
                    start_time_pup = pygame.time.get_ticks()  # Reset the start time for the power-up
                    print("Power-up applied!")
                elif pup_count == 2:
                    pup_count += 1
                    start_time_pup = pygame.time.get_ticks()  # Reset the start time for the power-up
                    print("Power-up applied!")
                elif pup_count == 4:
                    pup_count += 1
                    start_time_pup = pygame.time.get_ticks()  # Reset the start time for the power-up
                    print("Power-up applied!")

            elapsed_time_pup = (pygame.time.get_ticks() - start_time_pup) / 1000  # Elapsed time for power-up


            if elapsed_time_pup >= powerup._duration and (pup_count==1 or pup_count == 3 or pup_count == 5):  # After the duration
                powerup.remove(player,enemies) #remove power up from the player
                powerup._is_active = False
                pup_count +=1
                print("Power-up ended.")

        # Check player health
        if player.health <= 0:
            player.health = 100
            return "death"


        # Apply brightness and sound settings dynamically
        apply_brightness_and_sound(screen)
        pygame.display.flip()