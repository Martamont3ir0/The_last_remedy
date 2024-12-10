import pygame

from config import *

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
    #check mouse hover
    is_hover= rect.collidepoint(mouse_pos)
    is_clicked= pygame.mouse.get_pressed()[0]
    clicked_color= None

    #set button color based on state
    if is_hover and is_clicked and clicked_color: #left mouse button is pressed
        button_color= clicked_color
    elif is_hover:
        button_color= hover_color
    else:
        button_color= base_color

    #drawing the button rectangle with rounded corners:
    pygame.draw.rect(screen, button_color, rect, border_radius=border_radius)

    #drawing the button border
    pygame.draw.rect(screen, (0,100,0), rect, 3,border_radius=border_radius)


    #text
    button_text= font.render(text, True, text_color)
    text_rect= button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)

    #return True if clicked
    return rect

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







# Function to draw a stick figure with a construction hat
def draw_stick_figure_with_hat(screen, x, y):
    # head
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)  # White head outline

    # body
    pygame.draw.line(screen, (255, 255, 255), (x, y + 20), (x, y + 60), 2)  # Body

    # arms
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x - 30, y + 40), 2)  # Left arm
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x + 30, y + 40), 2)  # Right arm

    # legs
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x - 20, y + 100), 2)  # Left leg
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x + 20, y + 100), 2)  # Right leg

    # hat
    hat_color = (255, 215, 0)

    # drawing the construction hat
    pygame.draw.rect(screen, hat_color, [x - 25, y - 30, 50, 10])  # Hat's brim
    pygame.draw.rect(screen, hat_color, [x - 20, y - 40, 40, 20])  # Hat's dome


# Function to draw a normal stick figure (without a hat)
def draw_normal_stick_figure(screen, x, y):
    # head
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)  # White head outline

    # body
    pygame.draw.line(screen, (255, 255, 255), (x, y + 20), (x, y + 60), 2)  # Body

    # arms
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x - 30, y + 40), 2)  # Left arm
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x + 30, y + 40), 2)  # Right arm

    # legs
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x - 20, y + 100), 2)  # Left leg
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x + 20, y + 100), 2)  # Right leg


# Under construction screen
def under_construction(screen):

    # creating the screen at 720x720 pixels
    screen = pygame.display.set_mode(resolution)

    # setting up the fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)
    conversation_font = pygame.font.SysFont("Arial", 30)

    # setting my texts:
    back_text = corbelfont.render("back", True, white)
    construction_text = corbelfont.render("UNDER CONSTRUCTION", True, white)
    first_speech = conversation_font.render("Can we fix it?", True, white)
    bob_speech = conversation_font.render("Probably not...", True, white)

    # setting up the "images" positions
    bob_x_position = 460
    bob_y_position = 450

    normal_x_position = 260
    normal_y_position = 450

    # same old, same old while True loop

    while True:
        # getting the mouse position
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # checking if the back button was clicked
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    from interface import interface
                    interface()
                    return

        # displaying the screen:
        screen.fill(deep_black)

        # displaying the main UNDER CONSTRUCTION text
        construction_rect = construction_text.get_rect(center=(720 // 2, 300))
        screen.blit(construction_text, construction_rect)

        # drawing the back button
        pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # stick figures text and "images"
        draw_normal_stick_figure(screen, normal_x_position, normal_y_position)
        draw_stick_figure_with_hat(screen, bob_x_position, bob_y_position)

        screen.blit(first_speech, (normal_x_position - 60, normal_y_position -80))
        screen.blit(bob_speech, (bob_x_position - 60, bob_y_position - 80))

        # finally, as always, updating our screen
        pygame.display.update()


