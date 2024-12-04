from enemy import Enemy
from config import *
import pygame
from player import Player
from shed import shed


def character_selection_screen():
    # Screen setup
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Character Selection")

    # Load character images
    girl_image = pygame.image.load("class1_ui/img/lucaquinn_female.jpg")  # Correct image path for girl character
    boy_image = pygame.image.load("class1_ui/img/lucaquinn_male.jpg")  # Correct image path for boy character

    # Scale images
    girl_image = pygame.transform.scale(girl_image, (150, 150))
    boy_image = pygame.transform.scale(boy_image, (150, 150))

    # Positions
    girl_rect = girl_image.get_rect(center=(width // 3, height // 2))
    boy_rect = boy_image.get_rect(center=(2 * width // 3, height // 2))

    selected_character = None  # To store the choice
    character_image_path = None  # Store the selected image path
    clock = pygame.time.Clock()

    while selected_character is None:
        screen.fill((0, 0, 0))  # Clear screen with black background

        # Draw instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Choose your character", True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, height // 4))
        screen.blit(text, text_rect)

        # Draw character images
        screen.blit(girl_image, girl_rect)
        screen.blit(boy_image, boy_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if girl_rect.collidepoint(event.pos):
                    selected_character = "girl"
                    character_image_path = "class1_ui/img/lucaquinn_female.jpg"
                elif boy_rect.collidepoint(event.pos):
                    selected_character = "boy"
                    character_image_path = "class1_ui/img/lucaquinn_male.jpg"

        pygame.display.flip()
        clock.tick(30)

    return character_image_path  # Return the image path


def game_loop():
    # Character selection
    selected_character = character_selection_screen()  # Returns image path

    # Debugging: Check if image path was correctly selected
    print(f"Character image path: {selected_character}")

    # SETUP:
    # Load the background image and get its size (bg_width, bg_height)
    background = pygame.image.load("class1_ui/img/backroundscenario.jpg")
    bg_width, bg_height = background.get_size()

    # Create the player with the selected image path
    player = Player(bg_width, bg_height, selected_character)

    # Optional: Load animations for the player (if sprite sheet available)
    # Uncomment this line if you have a sprite sheet
    # player.load_animation_frames("class1_ui/img/player_sprite_sheet.png", frame_width=50, frame_height=50)

    current_state = "main"  # Start in the main area

    while True:
        if current_state == "main":
            current_state = execute_game(player, selected_character)
        elif current_state == "shed":
            current_state = shed(player)


def execute_game(player: Player = None, character_image_path=None):
    # SETUP:
    background = pygame.image.load("class1_ui/img/backroundscenario.jpg")
    bg_width, bg_height = background.get_size()

    if player is None:
        player = Player(bg_width, bg_height, character_image_path)

    # Clock for frame rate control
    clock = pygame.time.Clock()

    # Screen setup
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")

    # Create sprite groups
    player_group = pygame.sprite.Group()
    player_group.add(player)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Enemy cooldown and background scrolling position
    enemy_cooldown = 0
    bg_x = 0

    running = True
    while running:
        clock.tick(fps)

        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Shooting (example for auto-shooting)
        player.shoot(bullets)

        # Spawning enemies every two seconds
        if enemy_cooldown <= 0:
            enemy = Enemy()
            enemies.add(enemy)
            enemy_cooldown = fps * 2

        enemy_cooldown -= 1

        # Update all entities
        player_group.update()
        bullets.update()
        enemies.update(player)

        # Move and draw the background
        bg_x -= player.speed
        if bg_x <= -bg_width:
            bg_x = 0
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + bg_width, 0))

        # Draw all sprites
        player_group.draw(screen)
        enemies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Draw player health bar
        player.draw_health_bar(screen)

        # Check collisions between bullets and enemies
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 5
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()

        # Transition to the shed if the player reaches the right edge
        if player.rect.right >= width:
            return "shed"

        pygame.display.flip()

    # End the game if loop terminates
    pygame.quit()






