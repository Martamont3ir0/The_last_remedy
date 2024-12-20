import pygame
from config import *
from utils import *
from player import Player
from start_message import *
from death import *
from user_info import *
from backpack import *
from shed_characters import *
from laser import Laser
from bullet import Bullet

def shed(player, selected_character, bg_width,overlay_visible, map_visible):
    # Basic setup
    # setting up the background:
    background = pygame.image.load("img/thewastesbg.jpeg")

    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    # Initialize player if not already done
    if player is None:
        player = Player(bg_width, selected_character)

    player.rect.left = 0
    backpack_img = pygame.image.load("img/backpack.png")
    backpack_img = pygame.transform.scale(backpack_img, (100, 100))
    backpack_rect = backpack_img.get_rect(topleft=(600, 20))  # Create a rect for the backpack image
    # setting up the player
    player_group = pygame.sprite.Group()
    player_group.add(player)

    bullets= pygame.sprite.Group()
    lasers= pygame.sprite.Group()
    # setting up the other characters

    coins_group = pygame.sprite.Group()
    for count in range(6):
        coin = Coin()
        coins_group.add(coin)

    cactus_group = pygame.sprite.Group()
    for count in range(8):
        cactus = Cactus()
        cactus_group.add(cactus)

    monster_ex = Monster()
    monster = pygame.sprite.Group()
    monster.add(monster_ex)

    #ensure player has user_laser attribute
    if not hasattr(player, 'use_laser'):
        player.use_laser= False

    #information for start message
    level2_title = "Level 2: 'The Wastes'"
    level2_description = ['Description for level 2','under construction....']

    # add desert music
    pygame.mixer.music.load("audio/desertbgmusic.wav")
    # Set the volume (0.0 to 1.0)
    pygame.mixer.music.set_volume(0.3)  # Sets the volume to 30%

    # Start a timer
    start_time = pygame.time.get_ticks()

    # Main loop
    running = True

    while running and overlay_visible:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        # Show level start message

        show_start_message(screen, level2_title, level2_description, background,player)

        if pygame.time.get_ticks() - start_time >= 1000:  # After 10 seconds, the loop of start message ends
            running = False

        # Update the display (if needed)
        pygame.display.flip()
    pygame.mixer.music.play(-1)  # Start playing music in a loop

    while True:

        clock.tick(fps)
        screen.blit(background, (0, 0))
        user_info(player,screen,False)
        # Check player health
        if player.health <= 0:
            player.health = 100
            return "death"

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Check for mouse button down event

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if backpack_rect.collidepoint(event.pos):# Check if backpack is clicked
                    player.user_laser= False
                    return "backpack"#Enter the backpack

                # Start laser on KEYDOWN (only on level 2)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.weapon == "Laser" and player.use_laser:
                    if not lasers:  # Fire laser if not already active
                        laser = Laser(player.rect)
                        lasers.add(laser)

                # Stop laser on KEYUP
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    lasers.empty()  # Remove the laser when SPACE is released


        #update and draw all sprites
        player_group.update()

        lasers.update(player)


        player_group.draw(screen)  # Draw the player on the screen
        #bullets.draw(screen)
        lasers.draw(screen)

        screen.blit(backpack_img,backpack_rect.topleft)# Blit the image at the top-left of the rect

        if overlay_visible:
            # Create a white overlay
            overlay = pygame.Surface(resolution)
            overlay.fill(white)  # Fill with white
            overlay.set_alpha(240)  # Set transparency (0-255)
            # Blit the overlay on top of the image
            screen.blit(overlay, (0, 0))
            font= pygame.font.Font(None, 24)
            instructions = font.render("Looks like the sun is really strong, how are you going to see?", True, deep_black)
            instructions_rect = instructions.get_rect()
            instructions_rect.center = (width // 2, 50)
            screen.blit(instructions, instructions_rect)
            # Show backpack on a specific position without the overlay
            screen.blit(backpack_img, backpack_rect.topleft)  # Blit the image at the top-left of the rect


        if map_visible:
            coins_group.draw(screen)
            cactus_group.draw(screen)
            font = pygame.font.Font(None, 20)
            instructions = font.render("You have no money or weapons. Catch the coins and watch out for the cactus!", True,deep_black)
            instructions_rect = instructions.get_rect()
            instructions_rect.center = (width// 2-30, 50)
            screen.blit(instructions, instructions_rect)
            monster.update()
            monster.draw(screen)
            warning_text = ""

            if monster_ex.distance() >= 0: #the monster is not yet in the screen
                warning_text = f"Something in a {monster_ex.distance()} meters radar approaching..."

            if monster_ex.rect.x == 900: #monster is near the screen
                pygame.mixer.music.stop()
                pygame.mixer.music.load("audio/monster.mp3")
                pygame.mixer.music.play(-1)  # Start playing  in a loop

            if monster_ex.rect.x <= 950:
                warning_text = "It's the desert monster who protects the Solanum! Make sure you're not empty handed."

            warning = font.render(warning_text, True, deep_black)
            warning_rect = warning.get_rect()
            warning_rect.center = (width // 2 - 50, 90)
            screen.blit(warning, warning_rect)

            # Cactus collisions

            collided_cactus = pygame.sprite.spritecollide(player, cactus_group, False)
            if collided_cactus:
                player.take_damage(10, False)
                for cactus in collided_cactus:
                    cactus.kill()

            # Coins collisions

            collided_coins = pygame.sprite.spritecollide(player, coins_group, False)
            if collided_coins:
                player.money += 30
                for coin in collided_coins:
                    coin.kill()

            #Monster collisions

            collided_monster = pygame.sprite.spritecollide(player, monster, False)
            if collided_monster:
                return "death"


        # Apply brightness and sound settings dynamically
        apply_brightness_and_sound(screen)

        pygame.display.flip()

