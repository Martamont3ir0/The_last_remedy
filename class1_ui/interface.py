import pygame
from game import game_loop
from utils import *  # no need to import pygame because the import is in utils
from config import *  # importing colors and the like
from utils import under_construction
from PIL import Image
import textwrap #split long lines of text into shorter ones based on screen width
import time #for timing effect



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
    #current_y=y
    wrapped_lines=[]
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
                #rendered_line = font.render(wrapped_line, True, color)
                #screen.blit(rendered_line, (x, current_y))
                #current_y += line_spacing
                wrapped_lines.append(wrapped_line)
                wrapped_line = word  # Start the next line with the current word

        # Render any remaining text in the line
        if wrapped_line:
            wrapped_lines.append(wrapped_line)
            #rendered_line = font.render(wrapped_line, True, color)
            #screen.blit(rendered_line, (x, current_y))
            #current_y += line_spacing
    #calculate the total height of the text block
    total_height= len(wrapped_lines)* line_spacing
    start_y= (height-total_height)//2 #center vertically

    #each wrapped line needs to be centered horizontally
    for i, line in enumerate(wrapped_lines):
        rendered_line= font.render(line,True, color)
        line_width= rendered_line.get_width()
        line_x= (width-line_width)//2 #center horizontally
        screen.blit(rendered_line, (line_x, start_y+i*line_spacing))




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

def confirm_quit(screen):
    """
    Handles the quit confirmation dialog
    """

    #capture the current screen
    background= screen.copy()

    #dimensions for the confirmation box
    confirm_width, confirm_height= 450,250
    confirm_x= (width- confirm_width)//2
    confirm_y= (height-confirm_height)//2

    #create the box and text font
    confirm_box= pygame.Rect(confirm_x, confirm_y, confirm_width, confirm_height)
    dialog_font= pygame.font.SysFont("bookantiqua", 32)
    button_font= pygame.font.SysFont("bookantiqua", 30)

    #button dimensions and positions
    button_width, button_height= 120,50
    yes_button= pygame.Rect(
        confirm_x+50, confirm_y+confirm_height-80, button_width, button_height
    )
    no_button= pygame.Rect(
        confirm_x+confirm_width-50-button_width,
        confirm_y+confirm_height-80,
        button_width,
        button_height
    )
    clicked_button=None

    while True:
        mouse= pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit()
                return False
            if ev.type==pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(mouse):
                    clicked_button= "Yes"
                elif no_button.collidepoint(mouse):
                    clicked_button="No"
            elif ev.type==pygame.MOUSEBUTTONUP:
                if clicked_button=="Yes" and yes_button.collidepoint(mouse):
                    return False
                elif clicked_button=="No" and no_button.collidepoint(mouse):
                    return True
                clicked_button=None

        #drawing dimmed background
        screen.blit(background, (0,0))
        dim_overlay= pygame.Surface(resolution, pygame.SRCALPHA)
        dim_overlay.fill((0,0,0,180)) #semi-transparent black
        screen.blit(dim_overlay, (0,0))

        #drawing confirmation dialog box
        pygame.draw.rect(screen, (50,50,50), confirm_box, border_radius=15)
        pygame.draw.rect(screen, white, confirm_box, 4, border_radius=15)

        #drawing dialog text
        dialog_text= dialog_font.render(
            "Are you sure you want to quit?", True, white
        )
        dialog_rect= dialog_text.get_rect(center=(width//2, confirm_y+90))
        screen.blit(dialog_text, dialog_rect)

        #drawing the yes or no buttons for quitting
        is_hover_yes= yes_button.collidepoint(mouse)
        is_clicked_yes=clicked_button=="Yes"
        draw_buttons(
            screen=screen,
            text= "Yes",
            rect=yes_button,
            font=button_font,
            base_color=(169,169,169),
            text_color= white,
            hover_color=(173,216,230) if is_hover_yes else (169,169,169),
            mouse_pos= mouse
        )
        if is_clicked_yes:
            pygame.draw.rect(screen, (0,0,139), yes_button, border_radius=10)
            yes_text= button_font.render("Yes", True, white)
            yes_rect= yes_text.get_rect(center=yes_button.center)
            screen.blit(yes_text, yes_rect)

        is_hover_no= no_button.collidepoint(mouse)
        is_clicked_no= clicked_button=="No"
        draw_buttons(
            screen=screen,
            text="No",
            rect=no_button,
            font=button_font,
            base_color=(169,169,169) ,
            text_color=white,
            hover_color=(173,216,230)if is_hover_no else (169,169,169),
            mouse_pos= mouse
        )
        if is_clicked_no:
            pygame.draw.rect(screen, (0,0,139), no_button, border_radius=10)
            no_text= button_font.render("No", True, white)
            no_rect= no_text.get_rect(center=no_button.center)
            screen.blit(no_text,no_rect)

        pygame.display.update()


def interface():

    # initiating pygame
    pygame.init() # calling pygame

    # add background music
    pygame.mixer.music.load("audio/Star Wars IV A new hope - Binary Sunset (Force Theme).mp3")
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

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
    start_game_font = pygame.font.SysFont("perpetua", 50)  # script can ne another option

    clicked_button= None #tracking clicks

    #pulsing variables for start game button effect
    fade_alpha= 255 #start fully visible
    fade_delta= -5 #rate of fading

    # drawing the other buttons
    def other_buttons(text, x, y, hover_key, width=180, height=60):
        """
        creates a button with a filled rectangle and hover effects

        parameters:
        -text:text on the button
        -x,y: coordinates of the button's center
        -hover_key: key to track hover and clicked state
        -width, height:button's dimension

        returns:
        - pygame.Rect: the rectangle area for the button for hover and click detection
        """

        is_hover = x - width // 2 <= mouse[0] <= x + width // 2 and y - height // 2 <= mouse[1] <= y + height // 2
        is_clicked = clicked_button == hover_key

        # setting color based on the state of the button
        if is_clicked:
            text_color = white
            fill_color = (0, 200, 0)
        elif is_hover:
            text_color = white
            fill_color = (50, 255, 50)
        else:
            text_color = white
            fill_color = (0, 150, 0)


        rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        pygame.draw.rect(screen, fill_color, rect, border_radius=10)
        pygame.draw.rect(screen, (0, 255, 0), rect, width=3, border_radius=10)

        # for text
        button_text = bookantiqua.render(text, True, text_color)
        text_rect = button_text.get_rect(center=(x, y))
        screen.blit(button_text, text_rect)

        return rect

    while True:
        #getting the mouse position
        mouse= pygame.mouse.get_pos()

        #event detection
        for ev in pygame.event.get():
            #seeing if the user hits the red x button
            if ev.type==pygame.QUIT:
                pygame.quit()

            #check button clicks
            if ev.type==pygame.MOUSEBUTTONDOWN:
                #check if start game button is clicked
                if start_hover.collidepoint(mouse):
                    clicked_button= "Start Game"
                elif credits_hover.collidepoint(mouse):
                    clicked_button= "Credits"
                elif quit_hover.collidepoint(mouse):
                    clicked_button= "Quit"
                elif rules_hover.collidepoint(mouse):
                    clicked_button= "Rules"
                elif options_hover.collidepoint(mouse):
                    clicked_button= "Options"
            elif ev.type==pygame.MOUSEBUTTONUP:
                #handle button actions when mouse is released
                if clicked_button=="Start Game" and start_hover.collidepoint(mouse):
                    wilderness_explorer()
                    return
                elif clicked_button=="Credits" and credits_hover.collidepoint(mouse):
                    credits_()
                elif clicked_button=="Quit" and quit_hover.collidepoint(mouse):
                    if not confirm_quit(screen):
                        return

                elif clicked_button=="Rules" and rules_hover.collidepoint(mouse):
                    rules()
                    return
                elif clicked_button=="Options" and options_hover.collidepoint(mouse):
                    under_construction()
                    return
                clicked_button= None #reset the clicked button state


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

        #effect for start game button
        fade_alpha+=fade_delta
        if fade_alpha<=100 or fade_alpha>=255: #reverse fading direction
            fade_delta*= -1
        fade_alpha = max(100, min(255, fade_alpha)) #alpha value is between 100 and 255

        #drawing start game button
        start_button_x= width//2 #center it horizontally
        start_button_y= 340#vertical position for button
        is_hover = (start_button_x - 100 <= mouse[0] <= start_button_x + 100 and
                    start_button_y - 20 <= mouse[1] <= start_button_y + 20)
        is_clicked= clicked_button== "Start Game"
        if is_clicked:
            button_color= (200,50,50)
        elif is_hover:
            button_color= (128,128,128)
        else:
            button_color= white


        start_text= start_game_font.render("Start Game", True, button_color)
        start_text.set_alpha(fade_alpha) #set alpha for pulsing effect
        start_hover= start_text.get_rect(center=(start_button_x, start_button_y))
        screen.blit(start_text, start_hover)


        rules_hover = other_buttons("Rules", width//4,500,"Rules")
        options_hover= other_buttons("Options", width//4,600, "Options")
        credits_hover= other_buttons("Credits", (width//4)*3, 500, "Credits")
        quit_hover= other_buttons("Quit", (width//4)*3, 600, "Quit")

        # update the display so that the loop changes will appear
        pygame.display.update()
        pygame.time.delay(30) #speed of the pulse

def credits_():
    # basic settings
    screen = pygame.display.set_mode(resolution)


    # load the background image
    credits_bg = pygame.image.load('img/creditsbg.png')
    credits_bg = pygame.transform.scale(credits_bg, resolution)  # scale the image to match screen resolution

    # Create a semi-transparent overlay
    overlay = pygame.Surface(resolution, pygame.SRCALPHA)  # Create a surface with alpha channel
    overlay.fill((0, 0, 0, 128))  # Black with 50% opacity (alpha = 128)

    # creating the fonts:
    credits_font = pygame.font.SysFont("bookantiqua", 30)
    header_font= pygame.font.SysFont("bookantiqua", 50, bold=True)

    # credits text
    header_text = "'The Last Remedy' credits..."
    credits=[
        "Augusto Santos, ajrsantos@novaims.unl.pt",
        "Diogo Rastreio, drasteiro@novaims.unl.pt",
        "Liah Rosenfeld, lrosenfeld@novaims.unl.pt",
        "Marta Monteiro, 20231666@novaims.unl.pt",
        "Marta Trindade, 20231626@novaims.unl.pt",
        "Martim  Pereira, 20231663@novaims.unl.pt"
    ]

    #animation settings
    fade_alpha=0 #fade in effect of header
    scroll_y= height #starting point for scrolling credits
    scroll_speed= 1.5
    header_fade_out= False



    #button settings
    button_y= height-60 #align with the bottom of the screen
    back_x= width-150
    clicked_button= None


    # main loop to detect user input and displaying the credits page
    while True:
        # getting the position of the user's mouse
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            # allow the user to quit on (x)
            if ev.type == pygame.QUIT:
                pygame.quit()

            #detect button clicks
            elif ev.type==pygame.MOUSEBUTTONDOWN:
                if back_hover.collidepoint(mouse):
                    clicked_button= "Back To Menu"
            elif ev.type==pygame.MOUSEBUTTONUP:
                if clicked_button== "Back To Menu" and back_hover.collidepoint(mouse):
                    interface()
                    return
                    clicked_button= None #reset button state



        # displaying my screen
        screen.fill(deep_black)

        # displaying the background image
        screen.blit(credits_bg, (0, 0))
        screen.blit(overlay, (0, 0))

        #handle header fade in fade out
        if not header_fade_out:
            if fade_alpha<255:
                fade_alpha += 2  # fade in effect
            else:
                header_fade_out=True
        elif fade_alpha>0:
            fade_alpha-=2 #fade out effect


        header_surface= header_font.render(header_text, True, white)
        header_surface.set_alpha(fade_alpha)
        header_rect= header_surface.get_rect(center=(width//2, height//3))
        screen.blit(header_surface, header_rect)

        #start scrolling credits when the header is fully faded in
        if fade_alpha==255:
            header_fade_complete=True


        #scroll credits from bottom to top after fade in
        if header_fade_out or fade_alpha<255:
            for i, line in enumerate(credits):
                line_surface= credits_font.render(line,True, white)
                line_rect= line_surface.get_rect(center=(width//2,scroll_y+i*50))
                screen.blit(line_surface, line_rect)

            scroll_y-=scroll_speed #move the text upward
            if scroll_y + len(credits)*50<0:
              scroll_y= height

        #draw Back To Menu button
        is_hover = back_x - 70 <= mouse[0] <= back_x + 70 and button_y <= mouse[1] <= button_y + 40
        is_clicked= clicked_button== "Back To Menu"

        if is_clicked:
            button_color= (200,50,50) #grey color
        elif is_hover:
            button_color=  (128,128,128)
        else:
            button_color= white

        button_text= credits_font.render("Back To Menu", True, button_color)
        back_hover= button_text.get_rect(center=(back_x, button_y))
        screen.blit(button_text, back_hover)

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

    #colors:
    white= (255,255,255)
    button_color= (100,100,100)
    button_hover_color= (150,150,150)
    button_clicked_color= (200,50,50) #color when button is clicked

    # story paragraphs
    story_slides = [
        ["Background Story..."],
        ["The World is Dying.",
         "It’s 2032. ",
         "A global catastrophe: The Burn has torn the world ."],
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
        ["You play as  a former scientist who once worked on the Elixir project.",
        "The Coalition shut it down, erased the research, and destroyed your life. "],
        ["Now, after years of hiding, you’ve learned of the missing ingredient—Solanum—and its location deep within the Wastes,",
        "a desolate region devastated by radiation. If you can retrieve it, you can complete the Elixir and change the world."],
        ["But you’re not alone.",
        "The Coalition’s Sentinels will stop at nothing to prevent you from reaching the plant.",
        "And there are others—mercenaries, factions, and desperate survivors—who want the Elixir for themselves.",
        ""],
        ["In a dying world, everyone is a potential enemy."],
        ["Are you ready to save the world ? "]
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
        if slide_index==0: #special formatting for the first slide
            title_surface= header_font.render("Background Story...", True, white)
            title_rect= title_surface.get_rect(center=(width//2, height//3)) #center at the top
            screen.blit(title_surface, title_rect)
        else:

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

def wilderness_explorer():
    game_loop()


