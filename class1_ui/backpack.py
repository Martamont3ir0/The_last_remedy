from class1_ui.shed import shed
from config import *
from shed import *
import pygame
def backpack(screen,player,selected_character,bg_width):
    background = pygame.image.load("img/backpackchest.png")
    glasses = pygame.image.load("img/glasses.png")
    glasses = pygame.transform.scale(glasses, (200, 200))
    glasses_rect = glasses.get_rect(topleft=(80, 198))  # Create a rect for the glasses image
    while True:
        screen.blit(background, (0, 0))
        screen.blit(glasses, glasses_rect.topleft)  # Blit the image at the top-left of the rect
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # Check for mouse button down event

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if glasses_rect.collidepoint(event.pos):# Check if glasses are clicked
                    return shed(player,selected_character,bg_width,False) #return to the desert and without the overlay, aka sunlight

        pygame.display.flip()
