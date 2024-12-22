import pygame
from config import *
from utils import *
from player import Player
from start_message import *
from death import *
from user_info import *
from backpack import *
from shed_characters import *
from laser import Laser
from bullet import Bullet
from grenade import Grenade

def shed(player):
    # Basic setup
    # setting up the background:
    background = pygame.image.load("img/thewastesbg.jpeg")

    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    # Initialize player if not already done
    if player is None:
        player = Player()
    player.level = 2
    player.rect.left = 0
    backpack_img = pygame.image.load("img/backpack.png")
    backpack_img = pygame.transform.scale(backpack_img, (100, 100))
    backpack_rect = backpack_img.get_rect(topleft=(600, 20))  # Create a rect for the backpack image
    solanum = pygame.image.load("img/solanum.png")
    solanum = pygame.transform.scale(solanum,(100,180))

    # setting up active characters

    player_group = pygame.sprite.Group()
    player_group.add(player)
    lasers= pygame.sprite.Group()
    grenade = pygame.sprite.Group()
    monster = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    cactus_group = pygame.sprite.Group()


    if len(player.shed_characters.keys()) == 0:  # If characters haven't already been created
        # Store the monster instance as the key and its position as the value
        monster_ex = Monster()
        monster_pos = (monster_ex.rect.x, monster_ex.rect.y)
        player.shed_characters[monster_ex] = monster_pos  # Use the sprite instance as the key
        monster.add(monster_ex)

        # Create and add coins
        for count in range(6):
            coin = Coin()
            coin_pos = (coin.rect.x, coin.rect.y)
            coins_group.add(coin)
            player.shed_characters[coin] = coin_pos  # Use the sprite instance as the key

        # Create and add cacti
        for count in range(8):
            cactus = Cactus()
            cactus_pos = (cactus.rect.x, cactus.rect.y)
            cactus_group.add(cactus)
            player.shed_characters[cactus] = cactus_pos  # Use the sprite instance as the key
    else:
        # Update existing characters' positions and add them to groups
        for item, position in player.shed_characters.items():
            item.rect.x = position[0]  # Update x position
            item.rect.y = position[1]  # Update y position

            # Add to respective groups, depending on what class they correspond to
            if isinstance(item, Coin):
                coins_group.add(item)
            elif isinstance(item, Cactus):
                cactus_group.add(item)
            elif isinstance(item, Monster):
                monster_ex = item
                monster.add(item)

    #ensure player has user_laser attribute
    if not hasattr(player, 'use_laser'):
        player.use_laser= False

    #information for start message
    level2_title = "Level 2: 'The Wastes'"
    level2_description = [
    "Objective: Reach the Solanum plant and harvest it.",
    "Key Challenge: Navigate the desert using the map,",
    " avoiding or defeating whatever may hurt you.",
    "You have also gained access to your backpack and a shop.",
    "For your sake, explore it!"
]

    # add desert music
    pygame.mixer.music.load("audio/desertbgmusic.wav")
    # Set the volume (0.0 to 1.0)
    pygame.mixer.music.set_volume(0.3)  # Sets the volume to 30%

    # Start a timer
    start_time = pygame.time.get_ticks()

    # Main loop
    running = True


    while running and not player.seen_message2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            key = pygame.key.get_pressed()
            # 'P' logic for saving
            if key[pygame.K_p]:
                save_game(player, player.state)
        # Show level start message

        show_start_message(screen, level2_title, level2_description, background,player)

        if pygame.time.get_ticks() - start_time >= 10000:  # After 10 seconds, the loop of start message ends
            running = False
            player.seen_message2 = True

        # Update the display (if needed)
        pygame.display.flip()
    pygame.mixer.music.play(-1)  # Start playing music in a loop

    while True:

        clock.tick(fps)
        screen.blit(background, (0, 0))
        user_info(player,screen,False)
        # Check player health
        if player.health <= 0:
            player.health = 100
            return "death"

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            key = pygame.key.get_pressed()
            # 'P' logic for saving
            if key[pygame.K_p]:
                save_game(player, player.state)

        # Check for mouse button down event

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if backpack_rect.collidepoint(event.pos):# Check if backpack is clicked
                    player.user_laser= False
                    return "backpack"#Enter the backpack

                # Start laser on KEYDOWN (only on level 2)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.weapon == "Laser" and player.use_laser:
                    if not lasers:  # Fire laser if not already active
                        laser = Laser(player.rect)
                        lasers.add(laser)

                # Stop laser on KEYUP
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    lasers.empty()  # Remove the laser when SPACE is released

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if player.weapon == "Grenade":
                    target_pos = pygame.mouse.get_pos()
                    grenade_ex = Grenade(player.rect.x, player.rect.y, target_pos)
                    grenade.add(grenade_ex)





        #update and draw all sprites
        player_group.update(level=2)
        lasers.update(player)
        grenade.update(player)

        player_group.draw(screen)
        lasers.draw(screen)
        grenade.draw(screen)

        #Show backpack on a specific position
        screen.blit(backpack_img,backpack_rect.topleft)# Blit the image at the top-left of the rect

        if not player.glasses_used:
            # Create a white overlay
            overlay = pygame.Surface(resolution)
            overlay.fill(white)  # Fill with white
            overlay.set_alpha(240)  # Set transparency (0-255)
            # Blit the overlay on top of the image
            screen.blit(overlay, (0, 0))
            font= pygame.font.Font(None, 24)
            instructions = font.render("Looks like the sun is really strong, how are you going to see?", True, deep_black)
            instructions_rect = instructions.get_rect()
            instructions_rect.center = (width // 2, 50)
            screen.blit(instructions, instructions_rect)
            # Show backpack on a specific position without the overlay
            screen.blit(backpack_img, backpack_rect.topleft)  # Blit the image at the top-left of the rect


        if player.map_used:
            coins_group.draw(screen)
            cactus_group.draw(screen)
            font = pygame.font.Font(None, 20)
            instructions = font.render("Catch the coins to buy weapons and watch out for the cactus or other surprises!", True,deep_black)
            instructions_rect = instructions.get_rect()
            instructions_rect.center = (width// 2-30, 50)
            screen.blit(instructions, instructions_rect)
            stop_pos = (0,0)
            monster.update(stop_pos,player)
            monster.draw(screen)
            warning_text = ""

            if monster_ex.distance() >= 0: #the monster is not yet in the screen
                warning_text = f"Something in a {monster_ex.distance()} meters radar approaching..."

            if monster_ex.rect.x <= 900: #monster is near the screen
                pygame.mixer.music.stop()
                pygame.mixer.music.load("audio/monster.mp3")
                pygame.mixer.music.play(-1)  # Start playing  in a loop

            if monster_ex.rect.x <= 950 and monster_ex.is_alive:
                warning_text = "It's the desert monster who protects the Solanum! Make sure you're not empty handed."



            # Cactus collisions

            collided_cactus = pygame.sprite.spritecollide(player, cactus_group, False)
            if collided_cactus:
                player.take_damage(15, False)
                for cactus in collided_cactus:
                    cactus.kill()
                    # Remove the coin from the shed_characters dictionary using the sprite instance
                    if cactus in player.shed_characters:
                        player.shed_characters.pop(cactus)  # Use the sprite instance as the key

            # Coins collisions

            collided_coins = pygame.sprite.spritecollide(player, coins_group, False)
            if collided_coins:
                player.money += 35
                for coin in collided_coins:
                    coin.is_alive = False
                    coin.kill()
                    # Remove the coin from the shed_characters dictionary using the sprite instance
                    if coin in player.shed_characters:
                        player.shed_characters.pop(coin)  # Use the sprite instance as the key

            #Monster collisions

            collided_monster = pygame.sprite.spritecollide(player, monster, False)
            if collided_monster:
                if monster_ex.is_alive:
                    return "death"
                else:
                    return "level3"

            # Laser collisions
            for laser in lasers:
                cactus_laser = pygame.sprite.spritecollide(laser, cactus_group, False)
                if cactus_laser:
                    for cactus in cactus_laser:
                        cactus.kill()
                        cactus.is_alive = False
                        # Remove the coin from the shed_characters dictionary using the sprite instance
                        if cactus in player.shed_characters:
                            player.shed_characters.pop(cactus)  # Use the sprite instance as the key
                monster_laser = pygame.sprite.spritecollide(laser, monster, False)
                if monster_laser:
                    monster_ex.rect.x += 10

            #Grenade collisions
            for grenade_ex in grenade:
                monster_grenade = pygame.sprite.spritecollide(grenade_ex, monster,False)
                if monster_grenade:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("audio/grenade_sound.wav")
                    pygame.mixer.music.play(0)  # Play music once
                    player.weapon = "None"
                    monster_ex.image = solanum #changing the image of the monster to the image of solanum
                    stop_pos = grenade_ex.rect.topleft  # Making it stop where it was "killed"
                    monster_ex.kill_monster(stop_pos)  # Call the method to stop the monster
                    warning_text = "You've found Solanum! Harvest it to continue the mission."

            warning = font.render(warning_text, True, deep_black)
            warning_rect = warning.get_rect()
            warning_rect.center = (width // 2 - 50, 90)
            screen.blit(warning, warning_rect)


        # Apply brightness and sound settings dynamically
        apply_brightness_and_sound(screen)

        pygame.display.flip()

