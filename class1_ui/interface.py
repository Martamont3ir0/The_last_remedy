from game import game_loop
from utils import *  # no need to import pygame because the import is in utils
from config import *  # importing colors and the like
from utils import under_construction
from PIL import Image






def interface():

    # initiating pygame
    pygame.init() # calling pygame
    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution) # show the user something

    # setting the fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)
    comicsansfont = pygame.font.SysFont("Comic Sans MS", 50)

    # render the text (will be used in the game button)
    wilderness_text = corbelfont.render("Wilderness Explorer", True, white)
    quit_text = corbelfont.render("quit", True, white)
    rules_text = corbelfont.render("rules", True, white)
    options_text = corbelfont.render("options", True, white)
    credits_text = corbelfont.render("credits", True, white)
    title_text = comicsansfont.render("Computation III - Project", True, glowing_light_red)





    # main interface loop (will run until the user quits)
    while True:

        # getting the mouse position (future need)
        mouse = pygame.mouse.get_pos()

        # event detection (future work)
        for ev in pygame.event.get():
            # seeing if the user hits the red x button
            if ev.type == pygame.QUIT:
                pygame.quit()

            # quit button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    pygame.quit()

            # credits button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <590 and 480 <= mouse[1] <540:
                    credits_()

            # wilderness game button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 90 <= mouse[0] <= 630 and 240 <= mouse[1] <= 300:
                    wilderness_explorer()

            # options button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 90 <= mouse[0] <= 230 and 600 <= mouse[1] <= 660:
                    under_construction()

            # rules button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 90 <= mouse[0] <= 230 and 480 <= mouse[1] <= 540:
                    rules()


        # filling the screen
        screen.fill(deep_black)

        # wilderness explorer button
        pygame.draw.rect(screen, dark_red, [90, 240, 540, 60])
        wilderness_rect = wilderness_text.get_rect(center=(90 + 540 // 2, 240 + 60 // 2)) # text centered in the button
        screen.blit(wilderness_text, wilderness_rect)

        # rules button
        pygame.draw.rect(screen, grey, [90, 480, 140, 60])
        rules_rect = rules_text.get_rect(center=(90 + 140 // 2, 480 + 60 // 2))  # text centered in the button
        screen.blit(rules_text, rules_rect)

        # options button
        pygame.draw.rect(screen, grey, [90, 600, 140, 60])
        options_rect = options_text.get_rect(center=(90 + 140 // 2, 600 + 60 // 2))  # text centered in the button
        screen.blit(options_text, options_rect)

        # quit button
        pygame.draw.rect(screen, grey, [450, 600, 140, 60])
        quit_rect = quit_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))  # text centered in the button
        screen.blit(quit_text, quit_rect)

        # credits button
        pygame.draw.rect(screen, grey, [450, 480, 140, 60])
        credits_rect = credits_text.get_rect(center=(450 + 140 // 2, 480 + 60 // 2))  # text centered in the button
        screen.blit(credits_text, credits_rect)

        # showing the title of the project
        screen.blit(title_text, (55, 0))

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
    corbelfont = pygame.font.SysFont("Corbel", 50)
    comicsansfont = pygame.font.SysFont("Comic Sans MS", 25)

    # creating the rendered texts for the credits
    augusto_text = comicsansfont.render("Augusto Santos, ajrsantos@novaims.unl.pt", True, white)
    diogo_text = comicsansfont.render("Diogo Rastreio, drasteiro@novaims.unl.pt", True, white)
    liah_text = comicsansfont.render("Liah Rosenfeld, lrosenfeld@novaims.unl.pt", True, white)

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
        back_text = corbelfont.render("back", True, white)
        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # updating the display
        pygame.display.update()

def rules():
    # basic settings #

    screen = pygame.display.set_mode(resolution)

    # load the background image

    story_bg = pygame.image.load('images/backgroundstory.jpg')
    story_bg = pygame.transform.scale(story_bg, resolution)  # scale the image to match screen resolution

    # Create a semi-transparent overlay
    overlay = pygame.Surface(resolution, pygame.SRCALPHA)  # Create a surface with alpha channel
    overlay.fill((0, 0, 0, 128))  # Black with 50% opacity (alpha = 128)
    # creating the fonts:
    corbelfont = pygame.font.SysFont("Corbel", 20)
    comicsansfont = pygame.font.SysFont("Comic Sans MS", 12)

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
            rendered_line = comicsansfont.render(line, True, white)
            # Blit the rendered text onto the screen at the specified position
            screen.blit(rendered_line, (10, i))
            # Increment the y position for the next line
            i += 20  # Increase y position for next line (30 pixels apart)

        # drawing and displaying the back button
        pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        back_text = corbelfont.render("Back", True, white)
        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # updating the display
        pygame.display.update()

def wilderness_explorer():
    game_loop()

