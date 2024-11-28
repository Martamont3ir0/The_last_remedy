import pygame
from config import *
from utils import *
from utils import under_construction


def shed (player):
    #setup of the background and screen
    background= pygame.image.load("img/farm.png")
    background= pygame.transform.scale(background, resolution)
    screen= pygame.display.set_mode(resolution)
    clock=pygame.time.Clock()

    #set the players position to the left of the screen
    player.rect.left=0
    player_group= pygame.sprite.Group()
    player_group.add(player)

    special_area=pygame.Rect(530,30,140,140)

    running= True
    while running:
        clock.tick(fps)
        screen.blit(background, (0,0))

        #event handling
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        #update their position
        player.update()

        #detect if the user walks in the special area (House)
        if special_area.colliderect(player.rect):
            under_construction()
            #change player position to avoid infinte loo+
            player.rect.top=200
            player.rect.left=560

        #allow a player to return to the previous screen
        if player.rect.left<=0:
            #position the player to the right of the screen
            player.rect.left=width-player.rect.width
            return "main"

        #draw player
        player_group.draw(screen)

        pygame.display.flip()

