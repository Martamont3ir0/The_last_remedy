import pygame
from player import Player
from valve_mini_game import Valve
from button import Button
from elixir_vessel import ElixirVessel
from valve_mini_game import ValveMiniGame
from code_minigame import CodeEntryMiniGame
from elixir_minigame import ElixirMiniGame
from final_choice import FinalChoice


def run_level3(screen,player):

    # Level 3: "The Elixir"
    level3_title = "Level 3: 'The Elixir'"
    level3_description = [
        "Objective: Use the Elixir to decide humanity's fate.",
        "Setting: A ruined underground lab once belonging to The Last Dawn.",
        "Key Challenge: Fix the lab’s machinery to combine the Solanum with the Elixir.",
    ]

    # Stop background music from previous levels
    pygame.mixer.music.stop()


    # Background for Level 3
    background = pygame.image.load("img/lab_background.jpg")
    background = pygame.transform.scale(background, resolution)

    # Create player object
    if player is None:
        player = Player()

    # Create glowing puzzle objects
    valve = Valve(150, 400)  # Adjusted with example values
    button = Button(700, 400)  # Adjusted with example values
    elixir_vessel = ElixirVessel(400, 400)  # Adjusted with example values

    interactive_objects = pygame.sprite.Group(valve, button, elixir_vessel)

    # Start Level 3 music
    pygame.mixer.music.load("audio/lab_alarm.wav")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    # Flags for mini-games
    button_mini_game_active = False
    valve_mini_game_active = False
    button_solved = False  # Flag for button mini-game
    valve_solved = False  # Flag for valve mini-game

    # Main game loop
    running = True
    while running:

        dt = pygame.time.get_ticks() % 1000

        # Get the player's key states
        player_keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Handling user input for puzzles
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    valve.adjust_pressure(increase=True)
                elif event.key == pygame.K_DOWN:
                    valve.adjust_pressure(increase=False)
                elif event.key in range(pygame.K_0, pygame.K_9 + 1):  # Number keys for button code input
                    button.enter_code(chr(event.key))
                elif event.key == pygame.K_RETURN:
                    button.activate()
                    elixir_vessel.activate()

        # Valve mini-game logic
        if valve_mini_game_active:
            valve_mini_game = ValveMiniGame(valve, "img/valve_background.jpg")
            result = valve_mini_game.run(screen, pygame.time.Clock())
            if result == "solved":
                print("Valve mini-game completed!")
                valve_mini_game_active = False
                valve_solved = True  # Mark valve mini-game as solved

        # Button mini-game logic
        if button_mini_game_active:
            # Initialize the button mini-game only if it hasn't been initialized yet
            if 'mini_game' not in locals():
                mini_game = CodeEntryMiniGame("img/button_minigame.jpeg", "img/notebook_image.jpg",
                                              ["1666", "1626", "1633"])
                mini_game.mini_game_completed = False  # Ensure the mini-game isn't marked as completed initially

            # Run the button mini-game if it hasn't been completed
            if not mini_game.mini_game_completed:
                result = mini_game.run(screen, pygame.time.Clock())
                if result == "game":
                    print("Button mini-game completed!")
                    mini_game.mini_game_completed = True  # Lock the mini-game from being replayed
                    button_solved = True  # Mark button mini-game as solved
                    button_mini_game_active = False  # Deactivate the mini-game

        # Elixir mini-game logic
        if pygame.key.get_pressed()[pygame.K_e]:  # If the "E" key is pressed
            if elixir_vessel.is_near(player.rect, proximity=50):  # Check if player is near the elixir vessel
                if button_solved and valve_solved:  # Both mini-games must be solved to unlock the final mini-game
                    elixir_mini_game = ElixirMiniGame("img/vesselbackground.png",selected_character)
                    result = elixir_mini_game.run(screen, pygame.time.Clock())
                    if result == "completed":
                        print("Elixir mini-game completed! Level finished!")
                        running = False  # End the level once Elixir mini-game is completed
                        # Trigger the FinalChoice screen
                        final_choice_screen = FinalChoice(screen, player_character_image)
                        chosen_option = final_choice_screen.display_choice_screen()

                        # Show the outcome based on the player's choice
                        final_choice_screen.display_outcome_screen(chosen_option)

                else:
                    # Display a warning that other tasks must be completed first
                    warning_text = "Warning! Tasks incomplete."
                    font = pygame.font.Font(None, 48)

                    # Render text with white outline
                    outline_color = (255, 255, 255)  # White outline
                    text_color = (255, 0, 0)  # Red text
                    warning_surface_outline = font.render(warning_text, True, outline_color)
                    warning_surface = font.render(warning_text, True, text_color)

                    # Position the text
                    text_x = (screen.get_width() - warning_surface.get_width()) // 2
                    text_y = (screen.get_height() - warning_surface.get_height()) // 2

                    # Draw outline first (offset in 8 directions)
                    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]:
                        screen.blit(warning_surface_outline, (text_x + dx, text_y + dy))

                    # Draw main text
                    screen.blit(warning_surface, (text_x, text_y))

                    pygame.display.flip()
                    pygame.time.wait(2000)  # Show warning for 2 seconds

        # Check for interactions with the button
        if pygame.key.get_pressed()[pygame.K_e]:
            if button.is_near(player.rect, proximity=50):
                if not button_mini_game_active:
                    print("Interacting with button, starting mini-game!")
                    button_mini_game_active = True

        # Check for interactions with the valve
        if pygame.key.get_pressed()[pygame.K_e]:
            if valve.is_near(player.rect, proximity=50):
                if not valve_mini_game_active:
                    print("Interacting with valve, starting mini-game!")
                    valve_mini_game_active = True

        # Update glowing effects for puzzle objects
        button.update(dt)
        valve.update(player_keys)
        elixir_vessel.update(dt)

        # Update screen
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # Draw puzzle objects
        valve.draw(screen)
        button.draw(screen)
        elixir_vessel.draw(screen)

        # Draw interaction prompts and highlight logic
        for obj in interactive_objects:
            is_highlighted = False
            if obj.is_near(player.rect, proximity=50):
                is_highlighted = True
                font = pygame.font.Font(None, 36)
                interaction_prompt = font.render("Press E to interact", True, (255, 255, 255))
                obj.draw(screen, highlight=is_highlighted)

        # Draw the player
        player.update()
        screen.blit(player.image, player.rect)

        # Update the display
        pygame.display.flip()

        # Frame rate control
        pygame.time.delay(30)
    return player.selected_character  # Return the character type (either "girl" or "boy")
    pygame.mixer.music.stop()
    print("Level 3 setup complete!")
    return "end_game"









