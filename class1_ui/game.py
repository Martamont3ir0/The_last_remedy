from enemy import Enemy
from config import *
import pygame
from player import Player
from shed import shed


def game_loop():
    # Setup
    player = Player(width, height)  # Initialize player as None
    current_state = "main"  # Start in the main area

    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)


def execute_game(player: Player = None):
    # SETUP:

    # setting up the background:
    background = pygame.image.load("class1_ui/img/backroundscenario.jpg")
    bg_width, bg_height = background.get_size()  # Get the original size of the background image

    # using the clock to control the time frame.
    clock = pygame.time.Clock()

    # screen setup:
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")

    # Initialize the player if not already passed
    if player is None:
        player = Player(bg_width, bg_height)  # Pass bg_width and bg_height

    # Create sprite groups
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Bullet and enemy groups
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Enemy cooldown and background scrolling position
    enemy_cooldown = 0
    bg_x = 0

    # MAIN GAME LOOP
    running = True
    while running:
        # controlling the frame rate
        clock.tick(fps)

        # Move and draw the background
        bg_x -= player.speed
        if bg_x <= -bg_width:
            bg_x = 0
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + bg_width, 0))

        # handling events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Player shoots bullets
        player.shoot(bullets)

        # Spawn enemies every two seconds
        if enemy_cooldown <= 0:
            enemy = Enemy()
            enemies.add(enemy)
            enemy_cooldown = fps * 2
        enemy_cooldown -= 1

        # Update groups
        player_group.update()
        bullets.update()
        enemies.update(player)

        # Draw sprites
        player_group.draw(screen)
        enemies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Check collisions between bullets and enemies
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 5
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()

        # Transition to shed if player reaches the right edge
        if player.rect.right >= width:
            return "shed"

        pygame.display.flip()

    # End the game if loop terminates
    pygame.quit()





