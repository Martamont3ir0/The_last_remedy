import pygame
from config import *
from utils import *
from utils import under_construction


def shed(player):
    # Basic setup
    # setting up the background:
    background = pygame.image.load("img/farm.png")
    background = pygame.transform.scale(background, resolution)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    #set the players position to the left of the screen
    player.rect.left = 0
    player_group= pygame.sprite.Group()
    player_group.add(player)

    special_area = pygame.Rect(530, 30, 140, 140)

    running = True
    while running:
        clock.tick(fps)
        screen.blit(background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Update the player's position
        player.update()
        #detect if the user walks in the special area (House)
        if special_area.colliderect(player.rect):
            under_construction()  # Trigger the under_construction screen
            player.rect.top = 200  # Reset player position to prevent instant re-trigger
            player.rect.left = 560

        # Allow returning to the main screen
        if player.rect.left <= 0:
            #position the player to the right of the screen
            player.rect.left = width - player.rect.width
            return "main"  # Transition back to the main game

        # Draw player
        pygame.draw.rect(screen, cute_purple, player.rect)

        pygame.display.flip()