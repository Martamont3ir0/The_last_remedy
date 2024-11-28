from config import *
import math
import pygame
from player import Player
from  enemy import Enemy
from shed import shed

def game_loop():
    player= Player()
    current_state= "main"

    while True:
        if current_state=="main":
            current_state= execute_game(player)
        elif current_state== "shed":
            current_state=shed(player)


def execute_game(player:Player):
    """
    main function to execute the game loop
    """

    #clock for controling the frame rate
    clock=pygame.time.Clock()

    #screen background
    screen= pygame.display.set_mode(resolution)
    background= pygame.image.load("img/GRASS.jpg")
    background= pygame.transform.scale(background,(width,height))

    #screen setup
    screen=pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")


    #player setup
    #player= Player()
    player_group= pygame.sprite.Group()
    player_group.add(player)

    #initialize the bullet group
    bullets= pygame.sprite.Group()

    #initialize the enemy group
    enemies= pygame.sprite.Group()
    enemy_spawn_timer=0

    running= True
    while running:
        #control the fame rate
        clock.tick(fps)
        #fill the background
        screen.blit(background, (0,0))

        #event handling
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        #shooting
        player.shoot(bullets)

        #spawining the enemies
        if enemy_spawn_timer <=0:
            new_enemy= Enemy()
            enemies.add(new_enemy)
            enemy_spawn_timer= 2*fps #every two seconds


        #checking for the collisions between enemies and bullets
        for bullet in bullets:
            collided_enemies= pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health-=5
                bullet.kill()
                if enemy.health<=0:
                    enemy.kill() #destroy the enemy


        #update the enemy spawn timer
        #enemy_spawn_timer-=1


        # update positions
        player_group.update()
        bullets.update()
        enemies.update(player)

        #checking if the user goes into the shed area
        if player.rect.right>=width:
            #change the game state to shed
            return "shed"

        #drawing the objects
        player_group.draw(screen)
        enemies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        pygame.display.flip()
