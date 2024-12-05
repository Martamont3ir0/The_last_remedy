import pygame
from game import game_loop
from utils import *  # no need to import pygame because the import is in utils
from config import *  # importing colors and the like
from utils import under_construction
from PIL import Image

# glowing affect and shadow affect on title
def glowing_title(screen, title_font, text, position, text_color, glow_color,shadow_color):
    shadow_offset= 4
    shadow_surface= title_font.render(text, True, shadow_color)
    shadow_rect= shadow_surface.get_rect(center=(position[0]+shadow_offset,position[1]+shadow_offset))
    screen.blit(shadow_surface, shadow_rect.topleft)

    glow_levels= [6,8,10,12] #thickness of layer
    for level in glow_levels:
        glow_surface= title_font.render(text, True, glow_color)
        glow_rect= glow_surface.get_rect(center=position)
        #large layers
        glow_surface= pygame.transform.smoothscale(
            glow_surface,
            (glow_rect.width+level, glow_rect.height+level)
        )
        glow_rect= glow_surface.get_rect(center=position)
        screen.blit(glow_surface, glow_rect.topleft)

    title_surface= title_font.render(text, True, text_color)
    title_rect= title_surface.get_rect(center=position)
    screen.blit(title_surface, title_rect.topleft)



#trying to implement a function for drawing buttons
def draw_buttons (screen, text, rect, font,base_color, text_color, hover_color, mouse_pos, border_radius=15, padding=(20,10)):
    """
    drawing buttons with rounded corners, text and a hover effect
    Parameters:
    -screen: pygame display surface
    -text: text to display on the button
    -rect:pygame.Rect object is to define button size and position
    -font: font for text
    -base color: color of button
    -text color: color of text
    -hover color: color of button when hovered over
    -mouse pos: tuple of mouse position (x,y)
    -border radius: radius of rounded corners. Set to default 15
    -padding: tuple (horizontal, vertical) for text inside the button
    Returns:
        -bool: True if the button is clicked
                False if not
    """
    #change the button color when hovered
    if rect.collidepoint(mouse_pos):
        button_color= hover_color
    else:
        button_color= base_color

    #drawing the rounded rectangle button
    pygame.draw.rect(screen, button_color, rect, border_radius=border_radius)

    #padded rectangle button
    padded_rect= rect.inflate(padding[0], padding[1]) #padding to increase size
    pygame.draw.rect(screen, button_color, padded_rect, border_radius=border_radius)

    #text
    button_text= font.render(text, True, text_color)
    text_rect= button_text.get_rect(center=padded_rect.center)
    screen.blit(button_text, text_rect)

    #return True if clicked
    return rect.collidepoint(mouse_pos)





def interface():

    # initiating pygame
    pygame.init() # calling pygame
    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution) # show the user something

    # set background image for main screen
    main_background = pygame.image.load('class1_ui/img/main_background_screen.jpg')
    main_background = pygame.transform.scale(main_background, resolution)  # scale the image to match screen resolution

    #making the background more discrete
    overlay= pygame.Surface(resolution)
    overlay.set_alpha(128)
    overlay.fill((0,0,0))

    # setting the fonts
    bookantiqua = pygame.font.SysFont("bookantiqua", 50)
    title_font = pygame.font.SysFont("garamond", 80, bold=True, italic=True)

    # render the text (will be used in the game button)
    wilderness_text = bookantiqua.render("Start Game ", True, white)
    quit_text = bookantiqua.render("quit", True, white)
    rules_text = bookantiqua.render("rules", True, white)
    options_text = bookantiqua.render("options", True, white)
    credits_text = bookantiqua.render("credits", True, white)



    # main interface loop (will run until the user quits)
    while True:

        # getting the mouse position (future need)
        mouse = pygame.mouse.get_pos()

        # event detection (future work)
        for ev in pygame.event.get():
            # seeing if the user hits the red x button
            if ev.type == pygame.QUIT:
                pygame.quit()


        # filling the screen
        screen.fill(deep_black)

        # displaying the background image
        screen.blit(main_background, (0, 0))
        screen.blit(overlay, (0,0))

        #testing glowing affect
        glowing_title(
            screen,
            title_font,
            "The Last Remedy",
            (width//2,100),
            text_color=deep_black,
            glow_color=(0,255,0),
            shadow_color=white
        )
        #defining button rectangles
        start_button_rect = pygame.Rect(90, 240, 540, 60)
        rules_button_rect = pygame.Rect(90, 480, 140, 60)
        options_button_rect = pygame.Rect(90, 600, 140, 60)
        quit_button_rect = pygame.Rect(450, 600, 140, 60)
        credits_button_rect = pygame.Rect(450, 480, 140, 60)

        #drawing buttons and taking in consideration the interactions
        # quit button
        if draw_buttons(screen, "Quit", quit_button_rect, bookantiqua, grey, white, glowing_light_red, mouse):
            if ev.type == pygame.MOUSEBUTTONDOWN and quit_button_rect.collidepoint(mouse):
                pygame.quit()

        # credits button
        if draw_buttons(screen, "Credits", credits_button_rect, bookantiqua, grey, white, glowing_light_red, mouse):
            if ev.type == pygame.MOUSEBUTTONDOWN and credits_button_rect.collidepoint(mouse):
                credits_()

        # start  game button
        if draw_buttons(screen, "Start Game", start_button_rect, bookantiqua, dark_red, white, glowing_light_red,
                        mouse):
            if ev.type == pygame.MOUSEBUTTONDOWN and start_button_rect.collidepoint(mouse):
                wilderness_explorer()

        # options button
        if draw_buttons(screen, "Options", options_button_rect, bookantiqua, grey, white, glowing_light_red, mouse):
            if ev.type == pygame.MOUSEBUTTONDOWN and options_button_rect.collidepoint(mouse):
                under_construction()

        # rules button
        if draw_buttons(screen, "Rules", rules_button_rect, bookantiqua, grey, white, glowing_light_red, mouse):
            if ev.type == pygame.MOUSEBUTTONDOWN and rules_button_rect.collidepoint(mouse):
                rules()

        # update the display so that the loop changes will appear
        pygame.display.update()


def credits_():


    # basic settings #

    screen = pygame.display.set_mode(resolution)

    # add background music

    # Load your music file
    pygame.mixer.music.load("audio/Star Wars IV A new hope - Binary Sunset (Force Theme).mp3")
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

    # load the background image
    credits_bg = pygame.image.load('class1_ui/img/creditsbg.png')
    credits_bg = pygame.transform.scale(credits_bg, resolution)  # scale the image to match screen resolution

    # Create a semi-transparent overlay
    overlay = pygame.Surface(resolution, pygame.SRCALPHA)  # Create a surface with alpha channel
    overlay.fill((0, 0, 0, 128))  # Black with 50% opacity (alpha = 128)

    # creating the fonts:
    bookantiqua = pygame.font.SysFont("bookantiqua", 50)
    baskervilleoldface = pygame.font.SysFont("baskervilleoldface", 25)

    # creating the rendered texts for the credits
    augusto_text = bookantiqua.render("Augusto Santos, ajrsantos@novaims.unl.pt", True, white)
    diogo_text = bookantiqua.render("Diogo Rastreio, drasteiro@novaims.unl.pt", True, white)
    liah_text = bookantiqua.render("Liah Rosenfeld, lrosenfeld@novaims.unl.pt", True, white)

    # main loop to detect user input and displaying the credits page

    while True:
        # getting the position of the user's mouse
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            # allow the user to quit on (x)
            if ev.type == pygame.QUIT:
                pygame.quit()

            # checking if the user clicked the back button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    interface()

        # displaying my screen
        screen.fill(deep_black)

        # displaying the background image
        screen.blit(credits_bg, (0, 0))
        screen.blit(overlay, (0, 0))


        # displaying our texts
        screen.blit(augusto_text, (0, 0))
        screen.blit(diogo_text, (0, 25))
        screen.blit(liah_text, (0, 50))

        # drawing and displaying the back button
        pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        back_text = bookantiqua.render("back", True, white)
        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # updating the display
        pygame.display.update()

def rules():
    # basic settings #

    screen = pygame.display.set_mode(resolution)

    # load the background image

    story_bg = pygame.image.load('class1_ui/img/backgroundstory.jpg')
    story_bg = pygame.transform.scale(story_bg, resolution)  # scale the image to match screen resolution

    # Create a semi-transparent overlay
    overlay = pygame.Surface(resolution, pygame.SRCALPHA)  # Create a surface with alpha channel
    overlay.fill((0, 0, 0, 128))  # Black with 50% opacity (alpha = 128)
    # creating the fonts:
    bookantique = pygame.font.SysFont("bookantique", 20)
    baskervilleoldface = pygame.font.SysFont("baskervilleoldface", 14)

    # main loop to detect user input and displaying the rules page

    while True:
        # getting the position of the user's mouse
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            # allow the user to quit on (x)
            if ev.type == pygame.QUIT:
                pygame.quit()

            # checking if the user clicked the back button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    interface()

        # displaying my screen
        screen.fill(deep_black)

        # displaying the background image
        screen.blit(story_bg, (0, 0))
        screen.blit(overlay, (0, 0))

        # creating the rendered texts for the story
        story_text = [
            "Background Story",
            "",
            "The World is Dying.",
            "It’s 2032. A global catastrophe known as The Burn has torn the world apart.",
            "Years of environmental abuse and unchecked technological greed have caused Earth’s atmosphere to collapse,",
            "unleashing deadly solar radiation that scorches the land and turns entire cities to ash. The air is toxic,",
            "the oceans are poisoned, and humanity teeters on the edge of extinction.","",
            "But there is a way to save it all.",
            "The Elixir, a mysterious potion capable of reversing the damage of The Burn,",
            "was created in secret by an underground government project called The Last Dawn.",
            "The Elixir can heal the Earth, restore the environment, and stop the radiation from devouring the planet.",
            "But there’s a catch: the formula is incomplete, and only a single vial remains.",
            "Without a rare, missing ingredient called Solanum, the Elixir can’t be fully realized.",
            "",
            "The International Coalition, the global superpower, controls the remaining vial and plans to use it to consolidate their power.",
            "They are prepared to do whatever it takes to keep the Elixir under their thumb.",
            "",
            "You Are the Last Hope.",
            "You play as Luca Quinn, a former scientist who once worked on the Elixir project.",
            "The Coalition shut it down, erased the research, and destroyed your life. ",
            "Now, after years of hiding, you’ve learned of the missing ingredient—Solanum—and its location deep within the Wastes,",
            "a desolate region devastated by radiation. If you can retrieve it, you can complete the Elixir and change the world.",
            "",
            "But you’re not alone.",
            "The Coalition’s Sentinels will stop at nothing to prevent you from reaching the plant.",
            "And there are others—mercenaries, factions, and desperate survivors—who want the Elixir for themselves.",
            "",
            "In a dying world, everyone is a potential enemy."
        ]
        # displaying our texts
        i = 10  # Starting y position for text
        for line in story_text:
            # Render the line of text
            rendered_line = baskervilleoldface.render(line, True, white)
            # Blit the rendered text onto the screen at the specified position
            screen.blit(rendered_line, (10, i))
            # Increment the y position for the next line
            i += 20  # Increase y position for next line (30 pixels apart)

        # drawing and displaying the back button
        pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        back_text = bookantique.render("Back", True, white)
        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # updating the display
        pygame.display.update()

def wilderness_explorer():
    game_loop()

