import pygame
from game import game_loop
from utils import *  # no need to import pygame because the import is in utils
from config import *  # importing colors and the like
from utils import under_construction
from PIL import Image
import textwrap
#split long lines of text into shorter ones based on screen width

#function for text wrapping
def draw_slide(screen, slide, font, color, x,y, max_width, line_spacing):
    """
      Draws a slide on the screen, wrapping text based on the given max_width (in pixels).

    Parameters:
    - screen: pygame display surface
    - slide: list of strings to render
    - font: pygame font object
    - color: text color
    - x, y: starting position for the text
    - max_width: maximum width for text before wrapping (in pixels)
    - line_spacing: space between lines

    """
    current_y=y
    for line in slide:
        words = line.split(" ")
        wrapped_line = ""
        for word in words:
            # Add a space only if this isn't the first word in the line
            test_line = f"{wrapped_line} {word}" if wrapped_line else word

            # Check the width of the test line
            if font.size(test_line)[0] <= max_width:
                wrapped_line = test_line
            else:
                # Render the current line and move to the next line
                rendered_line = font.render(wrapped_line, True, color)
                screen.blit(rendered_line, (x, current_y))
                current_y += line_spacing
                wrapped_line = word  # Start the next line with the current word

        # Render any remaining text in the line
        if wrapped_line:
            rendered_line = font.render(wrapped_line, True, color)
            screen.blit(rendered_line, (x, current_y))
            current_y += line_spacing




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


    #text
    button_text= font.render(text, True, text_color)
    text_rect= button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)

    #return True if clicked
    return rect.collidepoint(mouse_pos)





def interface():

    # initiating pygame
    pygame.init() # calling pygame
    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution) # show the user something

    # set background image for main screen
    main_background = pygame.image.load('img/main_background_screen.jpg')
    main_background = pygame.transform.scale(main_background, resolution)  # scale the image to match screen resolution

    #making the background more discrete
    overlay= pygame.Surface(resolution)
    overlay.set_alpha(128)
    overlay.fill((0,0,0))

    # setting the fonts
    bookantiqua = pygame.font.SysFont("bookantiqua", 40)
    title_font = pygame.font.SysFont("garamond", 80, bold=True, italic=True)



    # main interface loop (will run until the user quits)
    while True:

        # getting the mouse position (future need)
        mouse = pygame.mouse.get_pos()

        # event detection (future work)
        for ev in pygame.event.get():
            # seeing if the user hits the red x button
            if ev.type == pygame.QUIT:
                pygame.quit()

            #check button clicks
            if ev.type==pygame.MOUSEBUTTONDOWN:
                #quit button
                if quit_button_rect.collidepoint(mouse):
                    pygame.quit()
                    return #exit the function cleanly
                #credits buttons
                if credits_button_rect.collidepoint(mouse):
                    credits_()
                    return #return to this function when back is clicked
                #start game button
                if start_button_rect.collidepoint(mouse):
                    wilderness_explorer()
                    return #return after the game loop
                #options button
                if options_button_rect.collidepoint(mouse):
                    under_construction()
                    return #return to this function when back is clicked
                if rules_button_rect.collidepoint(mouse):
                    rules()
                    return



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
        draw_buttons(screen, "Start Game", start_button_rect, bookantiqua, dark_red, white, glowing_light_red, mouse)

        rules_button_rect = pygame.Rect(90, 480, 140, 60)
        draw_buttons(screen, " Rules", rules_button_rect, bookantiqua, grey, white, glowing_light_red, mouse)

        options_button_rect = pygame.Rect(90, 600, 140, 60)
        draw_buttons(screen, "Options", options_button_rect, bookantiqua, grey, white, glowing_light_red, mouse)

        credits_button_rect = pygame.Rect(450, 480, 140, 60)
        draw_buttons(screen, "Credits", credits_button_rect, bookantiqua, grey, white, glowing_light_red, mouse)

        quit_button_rect = pygame.Rect(450, 600, 140, 60)
        draw_buttons(screen, "Quit", quit_button_rect, bookantiqua, grey, white, glowing_light_red, mouse)

        # update the display so that the loop changes will appear
        pygame.display.update()


def credits_():
    # basic settings
    screen = pygame.display.set_mode(resolution)

    # add background music
    pygame.mixer.music.load("audio/Star Wars IV A new hope - Binary Sunset (Force Theme).mp3")
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

    # load the background image
    credits_bg = pygame.image.load('img/creditsbg.png')
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
            if ev.type == pygame.MOUSEBUTTONDOWN and back_button_rect.collidepoint(mouse):
                interface()
                return


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
        back_button_rect= pygame.Rect(450,600,140,60)
        draw_buttons(screen, "Back", back_button_rect, bookantiqua, dark_red, white, glowing_light_red, mouse)
        #pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        #back_text = bookantiqua.render("back", True, white)
        #back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        #screen.blit(back_text, back_rect)

        # updating the display
        pygame.display.update()

def rules():
    # initialize screen
    screen = pygame.display.set_mode(resolution)

    # load the background image
    story_bg = pygame.image.load('img/backgroundstory.jpg')
    story_bg = pygame.transform.scale(story_bg, resolution)  # scale the image to match screen resolution

    # Create a semi-transparent overlay
    overlay = pygame.Surface(resolution, pygame.SRCALPHA)  # Create a surface with alpha channel
    overlay.fill((0, 0, 0, 128))  # Black with 50% opacity (alpha = 128)

    # creating the fonts:
    header_font= pygame.font.SysFont("timesnewroman", 50, bold=True)
    text_font= pygame.font.SysFont("timesnewroman", 25) #main content
    key_phrase_font= pygame.font.SysFont("timesnewroman", 25, italic=True) #emphasized text

    #colors:
    white= (255,255,255)
    button_color= (100,100,100)
    button_hover_color= (150,150,150)
    button_clicked_color= (200,50,50) #color when button is clicked

    # story paragraphs
    story_slides = [
        ["Background Story"],
        ["The World is Dying.","It’s 2032. A global catastrophe: The Burn has torn the world ."],
        ["Years of environmental abuse and unchecked technological greed have caused Earth’s atmosphere to collapse,",
        "unleashing deadly solar radiation that scorches the land and turns entire cities to ash."],
        ["The Elixir, a mysterious potion capable of reversing the damage of The Burn,"
        "was created in secret by an underground government project called The Last Dawn."],
        ["The Elixir can heal the Earth, restore the environment, and stop the radiation from devouring the planet.",
        "But there’s a catch: the formula is incomplete, and only a single vial remains."],
        ["Without a rare, missing ingredient called Solanum, the Elixir can’t be fully realized.",
        "The International Coalition, the global superpower, controls the remaining vial and plans to use it to consolidate their power.",
        "They are prepared to do whatever it takes to keep the Elixir under their thumb."],
        ["You Are the Last Hope."],
        ["You play as Luca Quinn, a former scientist who once worked on the Elixir project.",
        "The Coalition shut it down, erased the research, and destroyed your life. "],
        ["Now, after years of hiding, you’ve learned of the missing ingredient—Solanum—and its location deep within the Wastes,",
        "a desolate region devastated by radiation. If you can retrieve it, you can complete the Elixir and change the world."],
        ["But you’re not alone.",
        "The Coalition’s Sentinels will stop at nothing to prevent you from reaching the plant.",
        "And there are others—mercenaries, factions, and desperate survivors—who want the Elixir for themselves.",
        ""],
        ["In a dying world, everyone is a potential enemy."]
    ]

    slide_index= 0
    clock= pygame.time.Clock()
    clicked_button= None #tracking when the button is being clicked

    def draw_buttons(text,x, y, is_hover=False, is_clicked=False ):
        """
        drawing text button with hover and clicked effects
        """
        if is_clicked:
            color=button_clicked_color
        elif is_hover:
            color= button_hover_color
        else:
            color= button_color

        button_text= text_font.render(text, True, color)
        screen.blit(button_text, (x,y))
        text_width, text_height= text_font.size(text)
        return pygame.Rect(x,y, text_width, text_height)



    while True:
        mouse= pygame.mouse.get_pos()
        screen.blit(story_bg,(0,0))
        screen.blit(overlay,(0,0))



        #draw current slide
        slide= story_slides[slide_index]
        draw_slide(
            screen=screen,
            slide=slide,
            font=text_font,
            color=white,
            x=50,
            y=100,
            max_width= width-100,
            line_spacing=30
        )
        #y_offset=100
        #for line in slide:
            #if line== "Background Story": #header
                #rendered_line= header_font.render(line, True, white)
            #elif "The Burn" in line or "The Elixir" in line: #highlighting ket phrases
                #rendered_line= key_phrase_font.render(line, True, white)
            #else: #main content
                #rendered_line= text_font.render(line, True, white )
            #screen.blit(rendered_line, (50, y_offset))
            #y_offset+=40 #space between lines


        # button positions (centered at the bottom)
        button_y = height-60
        back_x = 50  # left aligned for back button
        prev_x= width//2#more spacing to the left
        next_x= width//2+220 #more spacing to the right



        #determining hover and clicked states for each button
        back_hover = draw_buttons(
            "Back To Menu", back_x, button_y,
            is_hover=(back_x<=mouse[0]<= back_x+ text_font.size("Back To Menu")[0]),
            is_clicked=(clicked_button =="Back To Menu")
        )

        prev_hover=draw_buttons("Previous", prev_x, button_y,
            is_hover=(prev_x<=mouse[0]<= prev_x+text_font.size("Previous")[0]),
            is_clicked=(clicked_button=="Previous")
        )
        next_hover=draw_buttons("Next", next_x, button_y,
            is_hover=(next_x <= mouse[0] <= next_x + text_font.size("Next")[0]),
            is_clicked=(clicked_button == "Next")
        )


        #Event handling
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit()
                return
            elif ev.type== pygame.MOUSEBUTTONDOWN:
                #detect which button is being clicked
                if back_hover.collidepoint(mouse):
                    clicked_button="Back To Menu"
                elif prev_hover.collidepoint(mouse):
                    clicked_button= "Previous"
                elif next_hover.collidepoint(mouse):
                    clicked_button= "Next"
            elif ev.type== pygame.MOUSEBUTTONUP:
                #handle button actions and reset the clicked button state
                if clicked_button=="Back To Menu" and back_hover.collidepoint(mouse):
                    interface()
                    return
                elif clicked_button== "Previous" and prev_hover.collidepoint(mouse) and slide_index>0:
                    slide_index-=1
                elif clicked_button== "Next" and next_hover.collidepoint(mouse) and slide_index <len(story_slides)-1:
                    slide_index+=1
                clicked_button= None #reset clicked state


        pygame.display.update()
        clock.tick(30)




