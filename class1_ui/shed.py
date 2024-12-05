import pygame
from config import *
from utils import *
from utils import under_construction
from player import Player

def shed(player, selected_character):
    # Basic setup
    # setting up the background:
    background = pygame.image.load("img/farm.png")
    background = pygame.transform.scale(background, (width, height))
    bg_width, bg_height = background.get_size()  # Get the dimensions of the background image
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

    running = True
    while running:
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

        # Allow returning to the main screen
        if player.rect.left <= 0:
            player.rect.left = width - player.rect.width
            return "main"  # Transition back to the main game



        pygame.display.flip()

