import pygame
from config import *
from utils import *
from user_info import *

def show_start_message(screen, level_title,level_description, background,player):
    """

    :param screen:
    :param level_title: string for level title
    :param level_description: string for level description
    :param background: image path loaded and ready to be displayed on the background
    :param:player in question, for the function user_info to work when called
    :return: shown message and background displayed
    """
    # setting up the background:
    screen.blit(background, (0, 0))

    # Apply brightness and sound settings dynamically
    apply_brightness_and_sound(screen)

    #Displaying where the user info will be but without the info yet
    user_info(player,screen,True)

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
    background_rect = None
    padding = 2

    i = 190  # Starting y position for text
    for line in level_description:
        # Render the line of text
        rendered_line = font.render(line, True, glowing_light_red)

        text_x = width//2-rendered_line.get_width() //2
        text_y = i
        # Create a background surface for the text
        background_rect = pygame.Rect(text_x - padding, text_y - padding,
                                   rendered_line.get_width() + 2 * padding,
                                   rendered_line.get_height() + 2 * padding)  # Add padding
        # Draw the background rectangle
        pygame.draw.rect(screen, deep_black, background_rect)  # Draw the background in red
        # Blit the rendered text onto the screen at the specified position
        screen.blit(rendered_line, (text_x, text_y))
        # Increment the y position for the next line
        i += 70  # Increase y position for next line (30 pixels apart)

    # Apply brightness and sound settings dynamically
    apply_brightness_and_sound(screen)

    pygame.display.flip()