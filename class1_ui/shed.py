import pygame
from config import *
from utils import *
from utils import under_construction
from player import Player
from start_message import *
from death import *
from user_info import *
from backpack import *

def shed(player, selected_character, bg_width,overlay_visible):
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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # Show level start message

        show_start_message(screen, level2_title, level2_description, background,player)

        if pygame.time.get_ticks() - start_time >= 10000:  # After 10 seconds, the loop of start message ends
            running = False

        # Update the display (if needed)
        pygame.display.flip()
    pygame.mixer.music.play(-1)  # Start playing music in a loop
    while True:

        clock.tick(fps)
        screen.blit(background, (0, 0))
        user_info(player,screen,False)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # Check for mouse button down event

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if backpack_rect.collidepoint(event.pos):# Check if backpack is clicked
                    backpack(player,selected_character,bg_width)#Enter the backpack

        player_group.draw(screen)  # Draw the player on the screen
        # Update the player's position
        player.update()
        #Show backpack on a specific position without the overlay
        screen.blit(backpack_img,backpack_rect.topleft)# Blit the image at the top-left of the rect

        if overlay_visible:
            # Create a white overlay
            overlay = pygame.Surface(resolution)
            overlay.fill(white)  # Fill with white
            overlay.set_alpha(200)  # Set transparency (0-255)
            # Blit the overlay on top of the image
            screen.blit(overlay, (0, 0))
            font= pygame.font.Font(None, 16)
            instructions = font.render("Looks like the sun is really strong, how are you going to see?", True, deep_black)
            instructions_rect = instructions.get_rect()
            instructions_rect.center = (width // 2, 50)
            screen.blit(instructions, instructions_rect)
            # Show backpack on a specific position without the overlay
            screen.blit(backpack_img, backpack_rect.topleft)  # Blit the image at the top-left of the rect


        pygame.display.flip()

