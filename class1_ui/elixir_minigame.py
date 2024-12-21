import pygame
from final_choice import FinalChoice
from game import *

class ElixirMiniGame:
    def __init__(self, background_path, character_type):
        self.character_type = character_type
        self.background = pygame.image.load('img/vesselbackground.png')  # Load the background image for the elixir mini-game
        self.font = pygame.font.Font(None, 48)  # Font for displaying text
        self.to_do_font = pygame.font.Font(None, 36)  # Font for to-do list
        self.ingredients = []  # To track the added ingredients
        self.recipe_steps = [
            "First, add Solanum (press S).",
            "Next, add Acid (press A).",
            "Then, add Water (press W).",
            "Finally, add a meaningful tear (press M)."
        ]
        self.current_step = 0  # Start with the first step

    def run(self, screen, clock, character_type):
        running = True
        while running:
            screen.fill((0, 0, 0))  # Clear the screen before drawing
            screen.blit(self.background, (0, 0))  # Draw the elixir background

            # Display the current recipe steps as a to-do list at the bottom
            for i, step in enumerate(self.recipe_steps):
                if i < self.current_step:
                    # If the step is completed, show it as crossed out
                    step_text = self.to_do_font.render(f"[x] {step}", True, (0, 255, 0))  # Green text
                else:
                    # Show incomplete steps as regular text
                    step_text = self.to_do_font.render(f"[ ] {step}", True, (255, 255, 255))  # White text

                # Position the to-do list at the bottom of the screen
                y_pos = screen.get_height() - 175 + i * 40  # Adjust vertical spacing to show at the bottom
                screen.blit(step_text, (50, y_pos))  # Draw the steps from the left side, but at the bottom

            # Display the recipe status on the screen (current step in the center)
            if self.current_step < len(self.recipe_steps):
                step_text = self.font.render(self.recipe_steps[self.current_step], True, (255, 255, 255))
                screen.blit(step_text, (screen.get_width() // 2 - step_text.get_width() // 2, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Handle ingredient addition based on key presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and self.current_step == 0:  # Solanum (S or s)
                        self.ingredients.append("Solanum")
                        self.current_step += 1  # Move to next step
                    elif event.key == pygame.K_a and self.current_step == 1:  # Acid (A or a)
                        self.ingredients.append("Acid")
                        self.current_step += 1
                    elif event.key == pygame.K_w and self.current_step == 2:  # Water (W or w)
                        self.ingredients.append("Water")
                        self.current_step += 1
                    elif event.key == pygame.K_m and self.current_step == 3:  # Meaningful Tear (M or m)
                        self.ingredients.append("Meaningful Tear")
                        self.current_step += 1  # The recipe is complete

            # Update the display
            pygame.display.flip()
            clock.tick(60)  # Limit the frame rate to 60 FPS

            # If the recipe is complete, return 'completed' to trigger the final choice
            if self.current_step == len(self.recipe_steps):
                pygame.time.wait(2000)  # Wait for 2 seconds before exiting mini-game
                running = False  # End the mini-game

        # Call the final choice mini-game after completion
        # Pass the character_type (which should be determined beforehand) to FinalChoice
        final_choice_screen = FinalChoice(screen, character_type)  # Now passing both arguments
        final_choice_screen.display_choice_screen()

        return 'completed'  # Signal that the mini-game is finished







