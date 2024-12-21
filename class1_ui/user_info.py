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

    # Apply brightness and sound settings dynamically
    apply_brightness_and_sound(screen)

    if during_message:
        font3 = pygame.font.Font(None, 24)
        data = "GATHERING PLAYER'S DATA..."
        data = font3.render(data,True,deep_black)
        data_rect = data.get_rect()
        data_rect.center = (width//2 , 645)
        screen.blit(data,data_rect)

    else:
        font2 = pygame.font.Font(None, 24)
        health_text = f"Health: {player.health}%"
        health_text = font2.render(health_text, True, deep_black)
        health_rect = health_text.get_rect()
        health_rect.center = (90, 620)
        screen.blit(health_text, health_rect)
        money_text = f"Money: {player.money} coins"
        money_text = font2.render(money_text, True, deep_black)
        money_rect = health_text.get_rect()
        money_rect.center = (90, 675)
        screen.blit(money_text, money_rect)
        weapon_text = f"Current weapon: {player.weapon}"
        weapon_text = font2.render(weapon_text, True, deep_black)
        weapon_rect = weapon_text.get_rect()
        weapon_rect.center = (545, 620)
        screen.blit(weapon_text, weapon_rect)
        pup_text = f"Current PowerUp: {player.pup}"
        pup_text = font2.render(pup_text, True, deep_black)
        pup_rect = pup_text.get_rect()
        pup_rect.center = (515, 675)
        screen.blit(pup_text, pup_rect)
