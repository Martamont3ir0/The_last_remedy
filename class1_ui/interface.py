from utils import * # no need to import pygame because the import is in utils
from config import * # importing colors and the like
from game import execute_game, game_loop
from utils import under_construction


def interface():
    # initiating pygame
    pygame.init()
    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution)

    corbel_font = pygame.font.SysFont("Corbel", 50)
    comicsans_font= pygame.font.SysFont("Comic Sans MS", 50)

    #Text
    wilderness_text = corbel_font.render("Wilderness Explorer", True, white)
    options_text= corbel_font.render("options", True, white)
    credits_text= corbel_font.render("credits", True, white)
    rules_text = corbel_font.render("rules", True, white)
    quit_text = corbel_font.render("quit", True, white)
    title_text = comicsans_font.render("Computation III -Project", True, glowing_light_red)


    #game loop
    while True:
        #event handling event is anything a user can do
        for ev in pygame.event.get():
            #quitting the game with the close button on the windows(x)
            if ev.type==pygame.QUIT:
                pygame.quit()

            #detecting if the user clicked on the quit button (45, 600 to 590, 660)
            if ev.type==pygame.MOUSEBUTTONDOWN:
                if 450<mouse[0]<=590 and 600<mouse[1]<=660:
                    #if the user clicks the quit button
                    pygame.quit()

            #detecting clicks on options(90,600 to 230, 660)
            if ev.type==pygame.MOUSEBUTTONDOWN:
                if 90<= mouse[0]<=230 and 600<=mouse[1]<=660:
                    #activate the function that makes the options screen
                    under_construction()

            if ev.type==pygame.MOUSEBUTTONDOWN:
                if 90<=mouse[0]<=230 and 480<=mouse[1]<=540:
                    under_construction()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 90 <= mouse[0] <= 630 and 240 <= mouse[1] <= 300:
                    wilderness_explorer()

            if ev.type==pygame.MOUSEBUTTONDOWN:
                if 450<=mouse[0]<=590 and 480<= mouse[1]<=540:
                    credits_()


        #background
        screen.fill(deep_black)

        #bunch of things

        # get the mouse information
        mouse = pygame.mouse.get_pos()

        #Buttons

        # Wilderness Explorer button
        pygame.draw.rect(screen, dark_red, [90, 240, 540, 60])
        # Text
        wilderness_rect = wilderness_text.get_rect(
            center = (90+540//2, 240+60//2)
        )
        # Writing
        screen.blit(wilderness_text, wilderness_rect)

        #rules
        pygame.draw.rect(screen, grey, [90,480,140,60])
        rules_rect = rules_text.get_rect(
            center= (90+140//2, 480+60//2)
        )
        screen.blit(rules_text, rules_rect)

        #options
        pygame.draw.rect(screen, grey, [90,600,140,60])
        options_rect= options_text.get_rect(
            center= (90+140//2, 600+60//2)
        )
        screen.blit(options_text, options_rect)

        #credits
        pygame.draw.rect(screen, grey, [450,480,140,60])
        credits_rect= credits_text.get_rect(
            center= (450+140//2, 480+60//2)
        )
        screen.blit(credits_text, credits_rect)

        #quit
        pygame.draw.rect(screen, grey, [450,600,140,60])
        quit_rect= quit_text.get_rect(
            center= (450+140//2, 600+60//2)
        )
        #display the title
        screen.blit(title_text, (55,0))

        screen.blit(quit_text, quit_rect)


        pygame.display.update()


# Under construction screen

def credits_():
    #base settings
    screen = pygame.display.set_mode(resolution)

    comicsansfont= pygame.font.SysFont("Comic Sans MS", 25)
    corbelfont=pygame.font.SysFont("Corbel", 50)

    augusto = comicsansfont.render("Augusto Santos, ajrsantos@novaims.unl.pt", True, white)
    diogo = comicsansfont.render("Diogo Rastreio, drasteiro@novaims.unl.pt", True, white)
    liah = comicsansfont.render("Liah Rosenfeld, lrosenfelt@novaims.unl.pt", True, white)

    while True:
        #detecting user input
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type== pygame.QUIT:
                pygame.quit()
            if ev.type== pygame.MOUSEBUTTONDOWN:
                if 450<=mouse[0]<= 590 and 600<= mouse[1]<=660:
                    interface()
        #displaying the credits
        screen.fill(deep_black)

        #displaying credits text
        screen.blit(augusto, (0,0))
        screen.blit(diogo, (0,25))
        screen.blit(liah, (0,50))

        #draw the back button
        #x, y, width, height
        pygame.draw.rect(screen, dark_red, [450,600,140,60])
        back_text= corbelfont.render("back", True, white)
        back_rect= back_text.get_rect(center=(450+140//2, 600+60//2))
        screen.blit(back_text, back_rect)

        #as always, updating my display
        pygame.display.update()


def rules_():
    print("Displaying rules...")

def wilderness_explorer():
    game_loop()
