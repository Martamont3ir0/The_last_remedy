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

def interface():
    """
contains the main user interface logic:
-menus
-navigation
-screen
-Main Menu, rules screen, credits
"""
    # Initialize Pygame
    pygame.init()

    # Create the screen and load assets
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("The Last Remedy")
    main_background = pygame.image.load(image_files["main_background"])
    main_background = pygame.transform.scale(main_background, resolution)
    overlay = pygame.Surface(resolution, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    # Play background music
    pygame.mixer.music.load("audio/Star Wars IV A new hope - Binary Sunset (Force Theme).mp3")
    pygame.mixer.music.play(-1)

    # Fonts
    bookantiqua = pygame.font.SysFont("bookantiqua", 40)
    title_font = pygame.font.SysFont(*fonts["title_font"])
    start_game_font = pygame.font.SysFont("perpetua", 50)

    # Variables
    fade_alpha = 255
    fade_delta = -5


    # Main loop
    while True:
        mouse = pygame.mouse.get_pos()

        # Event handling
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if start_hover.collidepoint(mouse):
                    game_loop(interface)
                    return
                elif credits_hover.collidepoint(mouse):
                    credits_(screen)
                    return
                elif quit_hover.collidepoint(mouse):
                    if not confirm_quit(screen):
                        return
                elif rules_hover.collidepoint(mouse):
                    rules(screen, main_background, overlay, title_font)
                    return
                elif options_hover.collidepoint(mouse):
                    setting_menus(screen)
            elif ev.type == pygame.MOUSEBUTTONUP:
                # Handle button clicks
                if start_hover.collidepoint(mouse):
                    game_loop(interface)
                    return
                elif  credits_hover.collidepoint(mouse):
                    credits_(screen)
                    return
                elif  quit_hover.collidepoint(mouse):
                    if not confirm_quit(screen):
                        return
                elif  rules_hover.collidepoint(mouse):
                    rules(screen, main_background, overlay, title_font)
                    return
                elif  options_hover.collidepoint(mouse):
                    under_construction(screen)
                    return

        # Draw background and overlay
        screen.fill(deep_black)
        screen.blit(main_background, (0, 0))
        screen.blit(overlay, (0, 0))

        # Title with glowing effect
        glowing_title(
            screen, title_font, "The Last Remedy",
            (resolution[0] // 2, 100), text_color=deep_black,
            glow_color=(0, 255, 0), shadow_color=white
        )

        # Pulsing Start Game button
        fade_alpha += fade_delta
        if fade_alpha <= 100 or fade_alpha >= 255:
            fade_delta *= -1
        fade_alpha = max(100, min(255, fade_alpha))

        start_button_x = resolution[0] // 2
        start_button_y = 340
        start_hover = pygame.Rect(start_button_x - 100, start_button_y - 20, 200, 40)
        is_hover = start_hover.collidepoint(mouse)
        start_button_color = (128, 255, 128) if is_hover else white
        start_text = start_game_font.render("Start Game", True, start_button_color)
        start_text.set_alpha(fade_alpha)
        screen.blit(start_text, start_hover.topleft)

        # Other buttons
        rules_hover = pygame.Rect(resolution[0] // 4 - 90, 500 - 30, 180, 60)
        options_hover = pygame.Rect(resolution[0] // 4 - 90, 600 - 30, 180, 60)
        credits_hover = pygame.Rect((resolution[0] // 4) * 3 - 90, 500 - 30, 180, 60)
        quit_hover = pygame.Rect((resolution[0] // 4) * 3 - 90, 600 - 30, 180, 60)

        draw_buttons(
            screen, "Story", rules_hover, bookantiqua,
            base_color=(0, 150, 0), text_color=white,
            hover_color=(50, 255, 50), mouse_pos=mouse
        )
        draw_buttons(
            screen, "Options", options_hover, bookantiqua,
            base_color=(0, 150, 0), text_color=white,
            hover_color=(50, 255, 50), mouse_pos=mouse
        )
        draw_buttons(
            screen, "Credits", credits_hover, bookantiqua,
            base_color=(0, 150, 0), text_color=white,
            hover_color=(50, 255, 50), mouse_pos=mouse
        )
        draw_buttons(
            screen, "Quit", quit_hover, bookantiqua,
            base_color=(0, 150, 0), text_color=white,
            hover_color=(50, 255, 50), mouse_pos=mouse
        )

        apply_brightness_and_sound(screen)
        # Update display
        pygame.display.update()
        pygame.time.delay(30)

def rules(screen, main_background, overlay, title_font):
    """
    Display the rules screen with background story slides.
    """
    # Story paragraphs
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
        ["Now, after years of hiding, you’ve learned of the missing ingredient—Solanum—and its location deep within the Wastes,",
         "a desolate region devastated by radiation. If you can retrieve it, you can complete the Elixir and change the world."],
        ["But you’re not alone.",
         "The Coalition’s Sentinels will stop at nothing to prevent you from reaching the plant.",
         "And there are others—mercenaries, factions, and desperate survivors—who want the Elixir for themselves."],
        ["In a dying world, everyone is a potential enemy."],
        ["Are you ready to save the world?"]
    ]

    text_font = pygame.font.SysFont("timesnewroman", 30)
    slide_index = 0
    clicked_button = None


    while True:
        mouse = pygame.mouse.get_pos()

        # Event handling
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if back_hover.collidepoint(mouse):
                    clicked_button = "Back To Menu"
                elif prev_hover.collidepoint(mouse):
                    clicked_button = "Previous"
                elif next_hover.collidepoint(mouse):
                    clicked_button = "Next"
            elif ev.type == pygame.MOUSEBUTTONUP:
                if clicked_button == "Back To Menu" and back_hover.collidepoint(mouse):
                    interface()
                    return
                elif clicked_button == "Previous" and prev_hover.collidepoint(mouse) and slide_index > 0:
                    slide_index -= 1
                elif clicked_button == "Next" and next_hover.collidepoint(mouse) and slide_index < len(story_slides) - 1:
                    slide_index += 1
                clicked_button = None

        # Draw the background and overlay
        screen.blit(main_background, (0, 0))
        screen.blit(overlay, (0, 0))

        # Draw the current slide
        slide = story_slides[slide_index]
        draw_slide(screen, slide, text_font, white, 50, 100, width- 100, 30)

        # Button positions
        button_y = resolution[1] - 60
        back_x = 50
        prev_x = resolution[0] // 2+100
        next_x = resolution[0] // 2 + 260

        #back to menu button
        back_hover= pygame.Rect(back_x, button_y, 150,40)
        is_hover_back= back_hover.collidepoint(mouse)
        back_text_color= (50,255,50) if is_hover_back else white
        back_text_surface= text_font.render("Back To Menu", True, back_text_color)
        screen.blit(back_text_surface, (back_x, button_y))

        #previous button
        prev_hover= pygame.Rect(prev_x, button_y, 100,40)
        is_hover_prev= prev_hover.collidepoint(mouse)
        prev_text_color= (50,255,50) if is_hover_prev else white
        prev_text_surface= text_font.render("Previous", True, prev_text_color)
        screen.blit(prev_text_surface, (prev_x, button_y))

        #next button
        next_hover= pygame.Rect(next_x, button_y, 100,40)
        is_hover_next= next_hover.collidepoint(mouse)
        next_text_color= (50,255,50) if is_hover_next else white
        next_text_surface= text_font.render("Next",True, next_text_color)
        screen.blit(next_text_surface, (next_x, button_y))

        # Update display
        pygame.display.update()




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
                    save_settings()
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



        # Update the screen
        pygame.display.update()

def wilderness_explorer():
    game_loop()