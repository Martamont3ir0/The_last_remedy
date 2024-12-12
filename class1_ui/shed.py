import pygame
from config import *
from utils import *
from utils import under_construction
from player import Player
from start_message import *
from death import *
from user_info import *

def shed(player, selected_character, bg_width):
    # Basic setup
    # setting up the background:
    background = pygame.image.load("img/thewastesbg.jpeg")

    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    # Initialize player if not already done
    if player is None:
        player = Player(bg_width, selected_character)

    player.rect.left = 0
    special_area = pygame.Rect(530, 30, 140, 140)

    # setting up the player
    player_group = pygame.sprite.Group()
    player_group.add(player)

    #information for start message
    level2_title = "Level 2: 'The Wastes'"
    level2_description = ['Description for level 2','under construction....']

    running = True
    show_message = True
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
                running = False
                pygame.quit()
        # Show level start message

        show_start_message(screen, level2_title, level2_description, background,player)

        if pygame.time.get_ticks() - start_time >= 10000:  # After 10 seconds, the loop of start message ends
            running = False

        # Update the display (if needed)
        pygame.display.flip()

    while True:
        pygame.mixer.music.play(-1)  # Start playing music in a loop
        clock.tick(fps)
        screen.blit(background, (0, 0))
        user_info(player,screen,False)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        player_group.draw(screen)  # Draw the player on the screen

        # Update the player's position
        player.update()

        if special_area.colliderect(player.rect):
            under_construction()  # Trigger the under_construction screen
            player.rect.top = 200  # Reset player position to prevent instant re-trigger
            player.rect.left = 560

        pygame.display.flip()

