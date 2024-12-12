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
    screen.blit(background,(0,570))
    if during_message:
        font3 = pygame.font.Font(None, 24)
        data = "GATHERING PLAYER'S DATA..."
        data = font3.render(data,True,deep_black)
        data_rect = data.get_rect()
        data_rect.center = (width//2 , 645)
        screen.blit(data,data_rect)

    else:
        font2 = pygame.font.Font(None, 25)
        health_text = f"Health: {player.health}%"
        health_text = font2.render(health_text, True, deep_black)
        health_rect = health_text.get_rect()
        health_rect.center = (80, 612)
        screen.blit(health_text, health_rect)
        money_text = f"Money:" #{player.money}%"
        money_text = font2.render(money_text, True, deep_black)
        money_rect = health_text.get_rect()
        money_rect.center = (80, 642)
        screen.blit(money_text, money_rect)
