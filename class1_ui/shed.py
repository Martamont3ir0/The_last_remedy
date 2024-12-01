import pygame
from config import *
from utils import *
from utils import under_construction


def shed(player):
    # Basic setup
    # setting up the background:
    background = pygame.image.load("images/farm.png")
    background = pygame.transform.scale(background, (width, height))
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    player.rect.left = 0

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

        if special_area.colliderect(player.rect):
            under_construction()  # Trigger the under_construction screen
            player.rect.top = 200  # Reset player position to prevent instant re-trigger
            player.rect.left = 560

        # Allow returning to the main screen
        if player.rect.left <= 0:
            player.rect.left = width - player.rect.width
            return "main"  # Transition back to the main game

        # Draw player
        pygame.draw.rect(screen, cute_purple, player.rect)

        pygame.display.flip()

