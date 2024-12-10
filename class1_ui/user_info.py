from config import *
import pygame


def user_info(player,screen,during_message):
    """
    function for display at the bottom the player's info
    :param player: player that is playing when calling the function
    :param screen: respective screen that is defined before calling the function
    :param during_message: boolean regarding if a message is being displayed or not
    :return: partial background and information of player
    """

    # Displaying player's health
    background = pygame.image.load("img/woodinfo.png")
    screen.blit(background,(0,552))
    if during_message:
        font3 = pygame.font.Font(None, 24)
        data = "GATHERING PLAYER'S DATA..."
        data = font3.render(data,True,deep_black)
        data_rect = data.get_rect()
        data_rect.center = (width//2 , 630)
        screen.blit(data,data_rect)

    else:
        font2 = pygame.font.Font(None, 23)
        health_text = f"Health: {player.health}%"
        health_text = font2.render(health_text, True, deep_black)
        health_rect = health_text.get_rect()
        health_rect.center = (70, 590)
        screen.blit(health_text, health_rect)
