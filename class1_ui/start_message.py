import pygame
from config import *
from utils import *

def show_start_message(screen, level_title,level_description, background):
    """

    :param screen:
    :param level_title: string for level title
    :param level_description: string for level description
    :param background: image path loaded and ready to be displayed on the background
    :return: shown message and background displayed
    """
    # setting up the background:
    screen.blit(background, (0, 0))

    # Display a start message
    font = pygame.font.Font(None, 26)
    font_title = pygame.font.Font(None, 80)
    level_title = font_title.render(level_title, True, greenish)
    text_rect = level_title.get_rect()  # Get the rectangle of the text surface

    # Center the text rectangle
    text_rect.center = (width // 2, 100)  # Center it

    # displaying our texts
    # Blit the level title onto the screen at the specified position
    screen.blit(level_title,text_rect)
    i = 190  # Starting y position for text
    for line in level_description:
        # Render the line of text
        rendered_line = font.render(line, True, glowing_light_red)
        # Blit the rendered text onto the screen at the specified position
        screen.blit(rendered_line, (15, i))
        # Increment the y position for the next line
        i += 70  # Increase y position for next line (30 pixels apart)
    pygame.display.flip()

    # handling events:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.time.delay(10000)  # Delay for 10000 milliseconds (10 seconds)
