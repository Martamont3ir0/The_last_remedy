from death import death
import pygame
from utils import (
    draw_buttons,
    confirm_quit,
    draw_slide,
    glowing_title,
    under_construction
)
from config import *
from game import *
from player import *

def interface():
    """
    Contains the main user interface logic for the game:
    - Manages menus
    - Handles navigation between screens
    - Displays the main menu, rules screen, and credits
    """
    # Initialize Pygame
    pygame.init()

    # Create the screen and load assets
    screen = pygame.display.set_mode(resolution)  # Set the screen size
    pygame.display.set_caption("The Last Remedy")  # Set the window title

    # Load and scale the main background image
    main_background = pygame.image.load(image_files["main_background"])
    main_background = pygame.transform.scale(main_background, resolution)

    # Create an overlay for the screen (for things like dimming during transitions)
    overlay = pygame.Surface(resolution, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent black overlay

    # Play background music (loops indefinitely)
    pygame.mixer.music.load("audio/Star Wars IV A new hope - Binary Sunset (Force Theme).mp3")
    pygame.mixer.music.play(-1)

    # Set up fonts for different UI text
    bookantiqua = pygame.font.SysFont("bookantiqua", 40)
    title_font = pygame.font.SysFont(*fonts["title_font"])
    start_game_font = pygame.font.SysFont("perpetua", 50)

    # Initialize variables for fade effects (e.g., fade-in/out)
    fade_alpha = 255
    fade_delta = -5  # Change in alpha value to control fade speed

    # Main loop for displaying the interface
    while True:
        mouse = pygame.mouse.get_pos()  # Get current mouse position

        # Event handling (listening for user input)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                # Handle quitting the game
                pygame.quit()
                return

            if ev.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse button down events (user clicks)
                if start_hover.collidepoint(mouse):  # Start button hover
                    # Attempt to load saved game state
                    save_data = load_game()
                    if save_data:
                        # Restore the player state from the saved data
                        player = Player(save_data["health"], save_data["money"], save_data["state"], save_data["character"], save_data["type"])
                    else:
                        # Create a default player if no saved game is found
                        player = Player(100, 10, "main", "img/female-removebg-preview.png", "Girl")  # Default character
                    game_loop(interface, player, save_data["state"])  # Start the game loop with the player
                    return

                elif credits_hover.collidepoint(mouse):  # Credits button hover
                    credits_(screen)  # Show the credits screen
                    return

                elif quit_hover.collidepoint(mouse):  # Quit button hover
                    if not confirm_quit(screen):  # Confirm quit action
                        return

                elif rules_hover.collidepoint(mouse):  # Rules button hover
                    rules(screen, main_background, overlay, title_font)  # Show the rules screen
                    return

                elif options_hover.collidepoint(mouse):  # Options button hover
                    setting_menus(screen)  # Show the settings/options menu

            elif ev.type == pygame.MOUSEBUTTONUP:
                # Handle mouse button release events (user has clicked and released)
                if start_hover.collidepoint(mouse):  # Start button clicked
                    game_loop(interface)  # Start the game loop
                    return
                elif credits_hover.collidepoint(mouse):  # Credits button clicked
                    credits_(screen)  # Show the credits screen
                    return
                elif quit_hover.collidepoint(mouse):  # Quit button clicked
                    if not confirm_quit(screen):  # Confirm quit action
                        return
                elif rules_hover.collidepoint(mouse):  # Rules button clicked
                    rules(screen, main_background, overlay, title_font)  # Show the rules screen
                    return
                elif options_hover.collidepoint(mouse):  # Options button clicked
                    under_construction(screen)  # Show "under construction" message
                    return

        # Draw background and overlay
        screen.fill(deep_black)  # Fill the screen with a deep black background
        screen.blit(main_background, (0, 0))  # Draw the main background image
        screen.blit(overlay, (0, 0))  # Apply a semi-transparent overlay for effects

        # Title with glowing effect
        glowing_title(
            screen, title_font, "The Last Remedy",  # Display the title text
            (resolution[0] // 2, 100),  # Position the title at the center horizontally, 100px from the top
            text_color=deep_black,  # Title text color (dark black)
            glow_color=(0, 255, 0),  # Green glow around the text
            shadow_color=white  # White shadow effect
        )

        # Pulsing Start Game button
        fade_alpha += fade_delta  # Change the fade alpha value for the pulsing effect
        if fade_alpha <= 100 or fade_alpha >= 255:  # If alpha is out of bounds, reverse the fade direction
            fade_delta *= -1
        fade_alpha = max(100, min(255, fade_alpha))  # Clamp the fade alpha value to stay within 100-255

        # Define the position and size of the "Start Game" button
        start_button_x = resolution[0] // 2  # Center the button horizontally
        start_button_y = 340  # Position the button 340px from the top
        start_hover = pygame.Rect(start_button_x - 100, start_button_y - 20, 200,
                                  40)  # Define the clickable area for the button
        is_hover = start_hover.collidepoint(mouse)  # Check if the mouse is hovering over the button
        start_button_color = (128, 255, 128) if is_hover else white  # Change button color if hovered
        start_text = start_game_font.render("Start Game", True, start_button_color)  # Render the text for the button
        start_text.set_alpha(fade_alpha)  # Set the alpha value to control the pulsing effect
        screen.blit(start_text, start_hover.topleft)  # Draw the "Start Game" button on the screen

        # Define the clickable areas for other buttons
        rules_hover = pygame.Rect(resolution[0] // 4 - 90, 500 - 30, 180, 60)  # "Rules" button position
        options_hover = pygame.Rect(resolution[0] // 4 - 90, 600 - 30, 180, 60)  # "Options" button position
        credits_hover = pygame.Rect((resolution[0] // 4) * 3 - 90, 500 - 30, 180, 60)  # "Credits" button position
        quit_hover = pygame.Rect((resolution[0] // 4) * 3 - 90, 600 - 30, 180, 60)  # "Quit" button position

        # Draw each button with the specified properties
        draw_buttons(
            screen, "Story", rules_hover, bookantiqua,  # Draw "Story" button
            base_color=(0, 150, 0), text_color=white,  # Default colors for the button
            hover_color=(50, 255, 50), mouse_pos=mouse  # Hover effect colors
        )
        draw_buttons(
            screen, "Options", options_hover, bookantiqua,  # Draw "Options" button
            base_color=(0, 150, 0), text_color=white,
            hover_color=(50, 255, 50), mouse_pos=mouse
        )
        draw_buttons(
            screen, "Credits", credits_hover, bookantiqua,  # Draw "Credits" button
            base_color=(0, 150, 0), text_color=white,
            hover_color=(50, 255, 50), mouse_pos=mouse
        )
        draw_buttons(
            screen, "Quit", quit_hover, bookantiqua,  # Draw "Quit" button
            base_color=(0, 150, 0), text_color=white,
            hover_color=(50, 255, 50), mouse_pos=mouse
        )

        # Apply any brightness or sound effects to the screen
        apply_brightness_and_sound(screen)

        # Update the display with the new changes
        pygame.display.update()

        # Add a short delay to control the refresh rate of the screen
        pygame.time.delay(30)


def rules(screen, main_background, overlay, title_font):
    """
    Display the rules screen with background story slides.

    This function handles the display of the rules screen, cycling through
    story slides that describe the game's plot and world. Users can navigate
    through the slides using 'Previous' and 'Next' buttons, or return to the
    main menu with the 'Back to Menu' button.
    """
    # Story paragraphs defining the background and plot of the game
    story_slides = [
        ["Background Story..."],
        ["The World is Dying.",
         "It’s 2032. ",
         "A global catastrophe: The Burn has torn the world apart."],
        ["Years of environmental abuse and unchecked technological greed have caused Earth’s atmosphere to collapse,",
         "unleashing deadly solar radiation that scorches the land and turns entire cities to ash."],
        ["The Elixir, a mysterious potion capable of reversing the damage of The Burn,",
         "was created in secret by an underground government project called The Last Dawn."],
        ["The Elixir can heal the Earth, restore the environment, and stop the radiation from devouring the planet.",
         "But there’s a catch: the formula is incomplete, and only a single vial remains."],
        ["Without a rare, missing ingredient called Solanum, the Elixir can’t be fully realized.",
         "The International Coalition, the global superpower, controls the remaining vial and plans to use it to consolidate their power.",
         "They are prepared to do whatever it takes to keep the Elixir under their thumb."],
        ["You Are the Last Hope."],
        ["You play as a former scientist who once worked on the Elixir project.",
         "The Coalition shut it down, erased the research, and destroyed your life."],
        [
            "Now, after years of hiding, you’ve learned of the missing ingredient—Solanum—and its location deep within the Wastes,",
            "a desolate region devastated by radiation. If you can retrieve it, you can complete the Elixir and change the world."],
        ["But you’re not alone.",
         "The Coalition’s Sentinels will stop at nothing to prevent you from reaching the plant.",
         "And there are others—mercenaries, factions, and desperate survivors—who want the Elixir for themselves."],
        ["In a dying world, everyone is a potential enemy."],
        ["Are you ready to save the world?"]
    ]

    text_font = pygame.font.SysFont("timesnewroman", 30)  # Font for the slide text
    slide_index = 0  # Index for tracking the current slide
    clicked_button = None  # Track the button clicked by the user

    while True:
        mouse = pygame.mouse.get_pos()  # Get the current mouse position

        # Event handling
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()  # Close the game if the user quits
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if back_hover.collidepoint(mouse):  # If clicked on 'Back To Menu'
                    clicked_button = "Back To Menu"
                elif prev_hover.collidepoint(mouse):  # If clicked on 'Previous'
                    clicked_button = "Previous"
                elif next_hover.collidepoint(mouse):  # If clicked on 'Next'
                    clicked_button = "Next"
            elif ev.type == pygame.MOUSEBUTTONUP:
                # Button actions on mouse button release
                if clicked_button == "Back To Menu" and back_hover.collidepoint(mouse):
                    interface()  # Go back to the main menu
                    return
                elif clicked_button == "Previous" and prev_hover.collidepoint(mouse) and slide_index > 0:
                    slide_index -= 1  # Go to the previous slide
                elif clicked_button == "Next" and next_hover.collidepoint(mouse) and slide_index < len(
                        story_slides) - 1:
                    slide_index += 1  # Go to the next slide
                clicked_button = None  # Reset clicked button

        # Draw the background and overlay
        screen.blit(main_background, (0, 0))  # Fill the screen with the main background image
        screen.blit(overlay, (0, 0))  # Apply the overlay on top for effects

        # Draw the current slide
        slide = story_slides[slide_index]  # Get the text for the current slide
        draw_slide(screen, slide, text_font, white, 50, 100, width - 100, 30)  # Draw the slide text

        # Button positions (bottom of the screen)
        button_y = resolution[1] - 60
        back_x = 50
        prev_x = resolution[0] // 2 + 100
        next_x = resolution[0] // 2 + 260

        # "Back to Menu" button
        back_hover = pygame.Rect(back_x, button_y, 150, 40)  # Rectangle for the button
        is_hover_back = back_hover.collidepoint(mouse)  # Check if mouse is hovering over the button
        back_text_color = (50, 255, 50) if is_hover_back else white  # Change color when hovered
        back_text_surface = text_font.render("Back To Menu", True, back_text_color)  # Render button text
        screen.blit(back_text_surface, (back_x, button_y))  # Display the button text

        # "Previous" button
        prev_hover = pygame.Rect(prev_x, button_y, 100, 40)
        is_hover_prev = prev_hover.collidepoint(mouse)
        prev_text_color = (50, 255, 50) if is_hover_prev else white
        prev_text_surface = text_font.render("Previous", True, prev_text_color)
        screen.blit(prev_text_surface, (prev_x, button_y))

        # "Next" button
        next_hover = pygame.Rect(next_x, button_y, 100, 40)
        is_hover_next = next_hover.collidepoint(mouse)
        next_text_color = (50, 255, 50) if is_hover_next else white
        next_text_surface = text_font.render("Next", True, next_text_color)
        screen.blit(next_text_surface, (next_x, button_y))

        # Apply brightness and sound settings dynamically
        apply_brightness_and_sound(screen)

        # Update the display
        pygame.display.update()  # Refresh the screen with the latest updates


def credits_(screen):
    """Display the credits screen."""
    credits_bg = pygame.image.load('img/creditsbg.png')
    credits_bg = pygame.transform.scale(credits_bg, resolution)
    overlay = pygame.Surface(resolution, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    credits_font = pygame.font.SysFont("bookantiqua", 30)
    header_font = pygame.font.SysFont("bookantiqua", 50, bold=True)
    header_text = "'The Last Remedy' credits..."
    credits_text = [ "Professors:",
        "Augusto Santos, ajrsantos@novaims.unl.pt",
        "Diogo Rastreio, drasteiro@novaims.unl.pt",
        "Liah Rosenfeld, lrosenfeld@novaims.unl.pt",
        "Coders :",
        "Marta Monteiro, 20231666@novaims.unl.pt",
        "Marta Trindade, 20231626@novaims.unl.pt",
        "Martim  Pereira, 20231663@novaims.unl.pt"
    ]

    fade_alpha = 0
    scroll_y = resolution[1]
    scroll_speed = 1.5
    header_fade_complete= False #controling fade out on header
    clicked_button = None

    while True:
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                clicked_button = "Back To Menu"
            elif ev.type == pygame.MOUSEBUTTONUP:
                if clicked_button == "Back To Menu":
                    interface()
                    return
                clicked_button=None

        screen.fill(deep_black)
        screen.blit(credits_bg, (0, 0))
        screen.blit(overlay, (0, 0))

        #header fade in, fade out
        if not header_fade_complete:
            if fade_alpha<255: #fade in
                fade_alpha+=2
            else:
                header_fade_complete = True #start fade out after full visibility
        elif fade_alpha>0:
            fade_alpha-=2 #fade out

        #render the header
        if fade_alpha>0:
            header_surface = header_font.render(header_text, True, white)
            header_surface.set_alpha(fade_alpha)
            header_rect = header_surface.get_rect(center=(resolution[0] // 2, resolution[1] // 3))
            screen.blit(header_surface, header_rect)

        #scroll credits text
        if header_fade_complete:
            for i, line in enumerate(credits_text):
                line_surface = credits_font.render(line, True, white)
                line_rect = line_surface.get_rect(center=(resolution[0] // 2, scroll_y + i * 50))
                screen.blit(line_surface, line_rect)

            scroll_y -= scroll_speed
            if scroll_y + len(credits_text) * 50 < 0:
                scroll_y = resolution[1]

        #drawing a back to menu button
        back_button_text= "Back To Menu"
        back_text_surface= credits_font.render(back_button_text, True , white)
        is_hover= pygame.Rect(resolution[0]-250, resolution[1]-60,200,40).collidepoint(mouse)

        #change text color on hover
        text_color= (50,255,50) if is_hover else white
        back_text_surface= credits_font.render(back_button_text, True, text_color)
        back_button_rect= back_text_surface.get_rect(center=(resolution[0]-150, resolution[1]-40))

        screen.blit(back_text_surface,back_button_rect)

        # Apply brightness and sound settings dynamically
        apply_brightness_and_sound(screen)

        pygame.display.update()

def setting_menus(screen):
    """
    Displays the settings menus with options for adjusting sound and brightness.
    """
    #Fonts
    title_font= pygame.font.SysFont("bookantiqua", 50)
    label_font= pygame.font.SysFont("bookantiqua", 30)


    # Slider positions
    volume_slider_rect = pygame.Rect(200, 200, 400, 10)
    brightness_slider_rect = pygame.Rect(200, 300, 400, 10)

    # Knob positions
    volume_knob_x = volume_slider_rect.left + game_settings["sound_volume"] * volume_slider_rect.width
    brightness_knob_x = brightness_slider_rect.left + game_settings["brightness"] * brightness_slider_rect.width

    dragging_volume = False
    dragging_brightness = False

    # "Back" button
    back_button = pygame.Rect(300, 500, 140, 50)


    # Main loop for the settings menu
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked on the volume knob
                if pygame.Rect(volume_knob_x - 10, volume_slider_rect.top - 5, 20, 20).collidepoint(mouse):
                    dragging_volume = True

                # Check if the user clicked on the brightness knob
                if pygame.Rect(brightness_knob_x - 10, brightness_slider_rect.top - 5, 20, 20).collidepoint(mouse):
                    dragging_brightness = True

                # Check if the user clicked the "Back" button
                if back_button.collidepoint(mouse):
                    return

            if event.type == pygame.MOUSEBUTTONUP:
                dragging_volume = False
                dragging_brightness = False


        # Adjust knob positions if dragging
        if dragging_volume:
            volume_knob_x = max(volume_slider_rect.left, min(mouse[0], volume_slider_rect.right))
            game_settings["sound_volume"]= (volume_knob_x-volume_slider_rect.left)/ volume_slider_rect.width
            pygame.mixer.music.set_volume(game_settings["sound_volume"])
        if dragging_brightness:
            brightness_knob_x = max(brightness_slider_rect.left, min(mouse[0], brightness_slider_rect.right))
            game_settings["brightness"]= (brightness_knob_x-brightness_slider_rect.left)/ brightness_slider_rect.width

        #update screen
        screen.fill(deep_black)

        #drawing tittle
        title_surface = title_font.render("Settings", True, white)
        screen.blit(title_surface, title_surface.get_rect(center=(width // 2, 100)))

        # Draw volume slider
        pygame.draw.rect(screen, (100, 100, 100), volume_slider_rect)  # Slider track
        pygame.draw.circle(screen, (200, 200, 200), (int(volume_knob_x), volume_slider_rect.centery), 10)  # Knob
        volume_text = label_font.render(f"Music Volume: {int(game_settings['sound_volume'] * 100)}%", True, white)
        screen.blit(volume_text, (volume_slider_rect.left, volume_slider_rect.top - 30))

        # Draw brightness slider
        pygame.draw.rect(screen, (100, 100, 100), brightness_slider_rect)  # Slider track
        pygame.draw.circle(screen, (200, 200, 200), (int(brightness_knob_x), brightness_slider_rect.centery),
                           10)  # Knob
        brightness_text = label_font.render(f"Brightness: {int(game_settings['brightness'] * 100)}%", True, white)
        screen.blit(brightness_text, (brightness_slider_rect.left, brightness_slider_rect.top - 30))

        # Adjust brightness using overlay
        brightness_overlay = pygame.Surface(resolution, pygame.SRCALPHA)
        brightness_overlay.fill((0, 0, 0, int((1 - game_settings['brightness']) * 255)))  # Dim the screen
        screen.blit(brightness_overlay, (0, 0))

        # Draw "Back" button
        pygame.draw.rect(screen, dark_red, back_button)
        back_text = label_font.render("Back", True, white)
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        # Apply brightness and sound settings dynamically
        apply_brightness_and_sound(screen)

        # Update the screen
        pygame.display.update()

def wilderness_explorer():
    game_loop()