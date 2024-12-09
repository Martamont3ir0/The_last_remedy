import pygame
from config import *
from utils import *

def death():
    """
    Player dies and screen resembles a death view.

    :return: user goes back to the main menu
    """
    #stop the background music
    pygame.mixer.music.stop()
    screen = pygame.display.set_mode(resolution)
    death = pygame.image.load("img/dyingstreet.jpeg")
    screen.blit(death,(0,0))

    # Display a message
    font = pygame.font.Font(None, 26)
    font_title = pygame.font.Font(None, 80)
    message_title = font_title.render("GAME OVER", True, dark_red)
    text_rect = message_title.get_rect()  # Get the rectangle of the text surface

    # Center the text rectangle
    text_rect.center = (width // 2, 100)  # Center it

    # displaying our texts
    # Blit the level title onto the screen at the specified position
    screen.blit(message_title,text_rect)
    i = 190  # Starting y position for text
    message_description = [
    "Luca Quinn, you’ve fallen.",
    "The Coalition’s taken control.",
    "The world’s hanging by a thread.",
    "If you don’t get back up, the darkness is gonna take over.",
    "Hope will vanish.",
    "The future of humanity is on the line.",
    "Are you ready to stand up and fight back, or is this where it all ends?"
]

    for line in message_description:
        # Render the line of text
        rendered_line = font.render(line, True, white)
        # Blit the rendered text onto the screen at the specified position
        screen.blit(rendered_line, (width//2-rendered_line.get_width() //2, i))
        # Increment the y position for the next line
        i += 50  # Increase y position for next line (30 pixels apart)

    # Update the display
    pygame.display.flip()

    # Wait for user input to return to the main menu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Exit the game
