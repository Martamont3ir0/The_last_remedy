import pygame
from final_choice import FinalChoice
from game import *


class ElixirMiniGame:
    def __init__(self):
        # Load the background image for the elixir mini-game
        self.background = pygame.image.load('img/vesselbackground.png')
        # Font for displaying text
        self.font = pygame.font.Font(None, 48)
        # Font for to-do list
        self.to_do_font = pygame.font.Font(None, 36)
        # To track the added ingredients
        self.ingredients = []
        # Recipe steps with instructions for adding ingredients
        self.recipe_steps = [
            "First, add Solanum (press S).",
            "Next, add Acid (press A).",
            "Then, add Water (press W).",
            "Finally, add a meaningful tear (press M)."
        ]
        # Start with the first step
        self.current_step = 0
        # Flag to show note or not
        self.note = False

    def run(self, screen, clock, player):
        # Font for the "Return" button
        font = pygame.font.Font(None, 26)
        back_text = font.render("Return", True, glowing_light_red)  # Text for "Return"
        back_text_rect = back_text.get_rect()  # Get the rectangle of the "Return" text
        back_text_rect.center = (30, 30)  # Position "Return" at the top-left of the screen
        running = True
        while running:
            screen.fill((0, 0, 0))  # Clear the screen before drawing
            screen.blit(self.background, (0, 0))  # Draw the elixir background
            screen.blit(back_text, back_text_rect)  # Draw the "Return" text

            # Display the current recipe steps as a to-do list at the bottom
            for i, step in enumerate(self.recipe_steps):
                if i < self.current_step:
                    # If the step is completed, show it as crossed out in green
                    step_text = self.to_do_font.render(f"[x] {step}", True, (0, 255, 0))
                else:
                    # Show incomplete steps as regular white text
                    step_text = self.to_do_font.render(f"[ ] {step}", True, (255, 255, 255))

                # Position the to-do list at the bottom of the screen with vertical spacing
                y_pos = screen.get_height() - 175 + i * 40
                screen.blit(step_text, (50, y_pos))  # Draw the steps from the left side, but at the bottom

            # Display the current recipe status (current step) in the center of the screen
            if self.current_step < len(self.recipe_steps):
                if not self.note:
                    # Display the current step
                    step_text = self.font.render(self.recipe_steps[self.current_step], True, (255, 255, 255))
                elif self.note:
                    # Display a note when the player is too insensitive
                    step_text = self.font.render("You're too insensitive, get PowerUp.", True, (255, 255, 255))
                screen.blit(step_text, (screen.get_width() // 2 - step_text.get_width() // 2, 50))

            # Event handling for quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Quit the game
                    exit()  # Exit the program

                # Handle ingredient addition based on key presses
                if event.type == pygame.KEYDOWN:
                    # Check if 'S' is pressed and if it's the first step in the recipe (Solanum)
                    if event.key == pygame.K_s and self.current_step == 0:
                        self.ingredients.append("Solanum")  # Add Solanum to ingredients
                        self.current_step += 1  # Move to next step in the recipe

                    # Check if 'A' is pressed and if it's the second step in the recipe (Acid)
                    elif event.key == pygame.K_a and self.current_step == 1:
                        self.ingredients.append("Acid")  # Add Acid to ingredients
                        self.current_step += 1  # Move to next step

                    # Check if 'W' is pressed and if it's the third step in the recipe (Water)
                    elif event.key == pygame.K_w and self.current_step == 2:
                        self.ingredients.append("Water")  # Add Water to ingredients
                        self.current_step += 1  # Move to next step

                    # Check if 'M' is pressed for the final step (Meaningful Tear), but only if the player feels "EXTRA Sad"
                    elif event.key == pygame.K_m and self.current_step == 3 and player.feelings != "EXTRA Sad":
                        self.note = True  # Display a note if the player is not in the required emotional state

                    # If player feels "EXTRA Sad" and presses 'M', add the Meaningful Tear ingredient
                    elif event.key == pygame.K_m and self.current_step == 3 and player.feelings == "EXTRA Sad":
                        self.note = False  # Remove the note
                        self.ingredients.append("Meaningful Tear")  # Add Meaningful Tear to ingredients
                        self.current_step += 1  # The recipe is complete

                # Handle mouse click for returning to the previous level
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                    if back_text_rect.collidepoint(event.pos):  # Check if return symbol is clicked
                        return "level 3"  # Return to level 3

                # Update the display and limit frame rate to 60 FPS
                pygame.display.flip()
                clock.tick(60)  # Limit the frame rate to 60 FPS

                # If the recipe is complete, trigger the end of the mini-game
                if self.current_step == len(self.recipe_steps):
                    pygame.time.wait(2000)  # Wait for 2 seconds before ending mini-game
                    running = False  # End the mini-game

                # Call the final choice mini-game after completion
                # Pass the character_type (which should be determined beforehand) to FinalChoice
                final_choice_screen = FinalChoice(screen, player)  # Now passing both arguments
                final_choice_screen.display_choice_screen()

                return 'completed'  # Signal that the mini-game is finished








