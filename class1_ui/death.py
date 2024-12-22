import pygame
from config import *
from utils import *


def death(interface_callback, player):
    """
    Player dies and screen resembles a death view.

    Displays a "Game Over" screen with a description of the player's fate.
    Provides options to restart the game or quit.

    :param interface_callback: A function used to handle the restart or quit action.
    :param player: The player object representing the current player in the game.

    :return: None
    """
    # Stop the background music
    pygame.mixer.music.stop()

    # Set up screen and background
    screen = pygame.display.set_mode(resolution)  # Set the display mode for the screen
    death_bg = pygame.image.load("img/dyingstreet.jpeg")  # Load the death background image
    death_bg = pygame.transform.scale(death_bg, resolution)  # Scale the image to the screen resolution

    # Define fonts for displaying messages
    font = pygame.font.Font(None, 26)  # Font for smaller text (e.g., description)
    font_title = pygame.font.Font(None, 80)  # Font for the title ("GAME OVER")
    button_font = pygame.font.SysFont("bookantiqua", 40)  # Font for button text

    # Title and description for the death screen
    message_title = font_title.render("GAME OVER", True, dark_red)  # Render the "Game Over" title text
    message_rect = message_title.get_rect(center=(width // 2, 100))  # Center the title at the top of the screen

    message_description = [
        "Luca Quinn, you’ve fallen.",
        "The Coalition’s taken control.",
        "The world’s hanging by a thread.",
        "If you don’t get back up, the darkness is gonna take over.",
        "Hope will vanish.",
        "The future of humanity is on the line.",
        "Are you ready to stand up and fight back, or is this where it all ends?"
    ]  # List of messages to display on the death screen

    # Button positions
    restart_button_x = width // 4  # Position for the restart button on the left
    quit_button_x = (width // 4) * 3  # Position for the quit button on the right
    button_y = resolution[1] - 100  # Vertical position for both buttons

    # Button surfaces and rects
    restart_text = "Restart Game"
    restart_surface = button_font.render(restart_text, True, white)  # Render the restart button text
    restart_rect = restart_surface.get_rect(center=(restart_button_x, button_y))  # Get the rect for the restart button

    quit_text = "Quit"
    quit_surface = button_font.render(quit_text, True, white)  # Render the quit button text
    quit_rect = quit_surface.get_rect(center=(quit_button_x, button_y))  # Get the rect for the quit button

    # Game loop
    player.health = 100  # Reset the player's health to 100
    waiting = True  # Set the waiting state to True, starting the loop
    while waiting:
        mouse = pygame.mouse.get_pos()  # Get the current mouse position
        for event in pygame.event.get():  # Process events
            if event.type == pygame.QUIT:  # If the quit event is triggered
                pygame.quit()  # Quit the game
                exit()

            elif event.type == pygame.MOUSEBUTTONUP:  # If the mouse button is released
                if restart_rect.collidepoint(event.pos):  # If the restart button is clicked
                    interface_callback()  # Call the interface callback to restart the game
                    return  # Exit the loop

                elif quit_rect.collidepoint(event.pos):  # If the quit button is clicked
                    if not confirm_quit(screen):  # Confirm if the player really wants to quit
                        pygame.quit()  # Quit the game
                        exit()

        key = pygame.key.get_pressed()  # Get the keys currently pressed
        # 'P' key logic for saving the game
        if key[pygame.K_p]:
            save_game(player, player.state)  # Save the game state

        # Drawing the background, title, and description
        screen.blit(death_bg, (0, 0))  # Draw the background image
        screen.blit(message_title, message_rect)  # Draw the title message

        y_offset = 190  # Starting y-offset for the description text
        for line in message_description:  # Loop through each line in the description
            line_surface = font.render(line, True, white)  # Render each line of text
            screen.blit(line_surface,
                        (width // 2 - line_surface.get_width() // 2, y_offset))  # Draw the line centered on the screen
            y_offset += 40  # Increase the y-offset for the next line

        # Drawing buttons with hover effects
        restart_color = (50, 255, 50) if restart_rect.collidepoint(mouse) else white  # Green when hovered, else white
        quit_color = (50, 255, 50) if quit_rect.collidepoint(mouse) else white  # Green when hovered, else white
        restart_surface = button_font.render(restart_text, True, restart_color)  # Render the restart button text
        quit_surface = button_font.render(quit_text, True, quit_color)  # Render the quit button text

        screen.blit(restart_surface, restart_rect)  # Draw the restart button
        screen.blit(quit_surface, quit_rect)  # Draw the quit button

        # Apply brightness and sound settings dynamically
        apply_brightness_and_sound(screen)

        pygame.display.update()  # Update the screen to reflect changes







