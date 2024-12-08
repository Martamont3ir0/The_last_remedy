import pygame
from config import *
from utils import *
from utils import under_construction
from player import Player
from start_message import *

def shed(player, selected_character, bg_width, bg_height):
    # Basic setup
    # setting up the background:
    background = pygame.image.load("img/thewastesbg.jpeg")

    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    # Initialize player if not already done
    if player is None:
        player = Player(bg_width, bg_height, selected_character)

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

    while running:
        #start by showing the level information
        if show_message:
            show_start_message(screen, level2_title, level2_description, background)
            pygame.display.flip()
            #after the function is implemented, boolean of show_message changes so that the game can continue
            show_message = False
        else:
            clock.tick(fps)
            screen.blit(background, (0, 0))

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

