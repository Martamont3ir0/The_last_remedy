import pygame
from config import *
from utils import *


def death(interface_callback,player):
    """
    Player dies and screen resembles a death view.

    :return: user goes back to the main menu
    """
    #stop the background music
    pygame.mixer.music.stop()
    #setup screen and background
    screen= pygame.display.set_mode(resolution)
    death_bg = pygame.image.load("img/dyingstreet.jpeg")
    death_bg = pygame.transform.scale(death_bg,resolution)


    # Display a message
    font = pygame.font.Font(None, 26)
    font_title = pygame.font.Font(None, 80)
    button_font= pygame.font.SysFont("bookantiqua", 40)

    #title and description
    message_title = font_title.render("GAME OVER", True, dark_red)
    message_rect = message_title.get_rect(center= (width//2,100))  # Get the rectangle of the text surface

    message_description = [
    "Luca Quinn, you’ve fallen.",
    "The Coalition’s taken control.",
    "The world’s hanging by a thread.",
    "If you don’t get back up, the darkness is gonna take over.",
    "Hope will vanish.",
    "The future of humanity is on the line.",
    "Are you ready to stand up and fight back, or is this where it all ends?"
    ]

    # Button positions
    restart_button_x= width//4 #position for restart game button on the left
    quit_button_x= (width//4)*3 #position for quit button on the right
    button_y= resolution[1]-100 #vertical position for both buttons


    # Button surfaces and rects
    restart_text = "Restart Game"
    restart_surface = button_font.render(restart_text, True, white)
    restart_rect = restart_surface.get_rect(center=(restart_button_x, button_y))

    quit_text = "Quit"
    quit_surface = button_font.render(quit_text, True, white)
    quit_rect = quit_surface.get_rect(center=(quit_button_x, button_y))

    #game loop
    player.health = 100 #reset health
    waiting=True
    while waiting:
        mouse=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                if restart_rect.collidepoint(event.pos):
                    interface_callback() #restart the game
                    return
                elif quit_rect.collidepoint(event.pos):
                    if not confirm_quit(screen):
                        pygame.quit()
                        exit()

        key = pygame.key.get_pressed()
        # 'P' logic for saving
        if key[pygame.K_p]:
            save_game(player, player.state)
        #drawing background, title and description
        screen.blit(death_bg, (0,0))
        screen.blit(message_title, message_rect)

        y_offset=190
        for line in message_description:
            line_surface= font.render(line, True, white)
            screen.blit(line_surface, (width//2-line_surface.get_width()//2, y_offset))
            y_offset+=40

        #drawing buttons with hover effects
        restart_color=(50,255,50) if restart_rect.collidepoint(mouse) else white
        quit_color= (50,255,50) if quit_rect.collidepoint(mouse) else white
        restart_surface= button_font.render(restart_text, True, restart_color)
        quit_surface= button_font.render(quit_text, True, quit_color)

        screen.blit(restart_surface, restart_rect)
        screen.blit(quit_surface, quit_rect)

        # Apply brightness and sound settings dynamically
        apply_brightness_and_sound(screen)

        pygame.display.update()






