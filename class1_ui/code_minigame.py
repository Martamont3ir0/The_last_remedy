import pygame
from config import *

class CodeEntryMiniGame:
    def __init__(self, background_path, notebook_image_path, valid_codes):
        self.background = pygame.image.load(background_path)

        # Load and scale the notebook image to be wider
        original_notebook_image = pygame.image.load('img/notebook_image.png')
        self.notebook_image = pygame.transform.scale(original_notebook_image, (475, 200))  # Wider notebook

        self.valid_codes = valid_codes
        self.input_text = ""  # The code being typed by the player

        # Load the custom handwritten font (use the .ttf font file) for the riddle text
        try:
            self.handwritten_font = pygame.font.Font("fonts/handwritten_font.ttf", 28)  # Slightly larger font
        except FileNotFoundError:
            print("Font file not found. Please make sure 'handwritten_font.ttf' is in the correct directory.")
            self.handwritten_font = pygame.font.Font(None, 28)  # Default font in case the custom font is missing
        except Exception as e:
            print(f"Error loading font: {e}")
            self.handwritten_font = pygame.font.Font(None, 28)  # Default font in case of any error

        self.font = pygame.font.Font(None, 48)  # Main font for game text
        self.small_font = pygame.font.Font(None, 32)  # Smaller font for UI text like feedback

        # Input box settings
        self.box_width = 125
        self.box_height = 50
        self.box_x = 300  # Position of the input box
        self.box_y = 300  # Position of the input box

        # Other variables
        self.solved = False  # Flag to indicate if the puzzle is solved
        self.active = False  # Whether the input box is active or not
        self.correct_codes_entered = []  # List to track entered valid codes (distinct)
        self.game_over = False  # Flag to indicate if the game is over

        # Flag to track if the mini-game has been solved and locked
        self.mini_game_completed = False  # To prevent the user from playing again

    def reset_game(self):
        # Reset the mini-game to the starting state
        self.correct_codes_entered = []  # Clear entered codes
        self.solved = False  # Reset puzzle solved flag
        self.game_over = False  # Reset game over flag
        self.input_text = ""  # Clear input text
        self.active = False  # Deactivate input box

    def run(self, screen, clock):
        running = True
        while running:
            # If the mini-game is completed, prevent interaction and show the solved screen
            if self.mini_game_completed:
                screen.fill((0, 0, 0))  # Black screen for "Code Corrected"
                solved_text = self.font.render("Code Corrected!", True, (0, 255, 0))  # Green text
                screen_center_x = screen.get_width() // 2
                screen_center_y = screen.get_height() // 2
                screen.blit(
                    solved_text,
                    (screen_center_x - solved_text.get_width() // 2, screen_center_y)
                )
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds
                return 'game'  # Exit to the main game after the message

            # Draw the background
            screen.fill((0, 0, 0))  # Clear the screen
            screen.blit(self.background, (-150, 0))  # Draw background image

            # Draw the scaled notebook image in the bottom-left corner
            notebook_x = 10  # 10 pixels from the left
            notebook_y = screen.get_height() - self.notebook_image.get_height() - 10  # Position at the bottom
            screen.blit(self.notebook_image, (notebook_x, notebook_y))

            # Display the riddle text on the notebook using the handwritten font
            riddle_lines = [
                "To solve this code, take note of these.",
                "The best students’ numbers will put you at ease.",
                "Insert them in order, don’t you deprive,",
                "Only then will you manage to survive.",
            ]
            start_y = notebook_y + 10  # Keep the start Y close to the notebook's top edge
            start_x = notebook_x + 65  # Start 65 pixels from the left side of the notebook
            for i, line in enumerate(riddle_lines):
                riddle_surface = self.handwritten_font.render(line, True, (0, 0, 0))  # Render the riddle text in black
                # Adjust the text position for each line
                screen.blit(riddle_surface, (start_x, start_y + i * 35))  # Adjust vertical offset for each line

            # Detect if mouse is hovering over the input box
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]  # Left mouse button pressed?

            # Highlight the box if mouse is hovering over it
            box_color = (255, 255, 255)  # Default box color
            if self.box_x <= mouse_x <= self.box_x + self.box_width and self.box_y <= mouse_y <= self.box_y + self.box_height:
                box_color = (200, 200, 200)  # Change to lighter color when hovering
                if mouse_clicked and not self.active and not self.mini_game_completed:  # Activate input box only if mini-game is not completed
                    self.active = True
                    self.input_text = ""  # Reset text on new activation

            # Draw the input box using the default font
            pygame.draw.rect(screen, box_color, (self.box_x, self.box_y, self.box_width, self.box_height), 2)
            input_surface = self.font.render(self.input_text, True, (255, 255, 255))
            screen.blit(input_surface, (self.box_x + 10, self.box_y + 10))  # Display the text inside the box

            # Check for player input if the box is active and mini-game is not completed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN and self.active:  # Only accept input if box is active
                    if event.key == pygame.K_BACKSPACE:  # Backspace key to delete character
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_RETURN:  # Enter key to submit the code
                        if self.input_text in self.valid_codes and self.input_text not in self.correct_codes_entered:  # Check if the code is valid and not entered before
                            self.correct_codes_entered.append(self.input_text)  # Add the correct code to the list
                            if len(self.correct_codes_entered) == len(self.valid_codes):  # Check if all codes are entered
                                self.solved = True  # All codes entered correctly, puzzle solved
                                pygame.time.wait(1000)  # Show a brief black screen for 1 second before success message
                            self.input_text = ""  # Reset the text box
                        else:
                            print("Incorrect code entered or already entered!")  # Feedback for duplicate codes
                            self.game_over = True  # Trigger game over when incorrect code is entered

                    elif event.key in range(pygame.K_0, pygame.K_9 + 1):  # Number keys (0-9)
                        if len(self.input_text) < 4:  # Limit input to 4 characters
                            self.input_text += chr(event.key)  # Add the number to the input text

            # Display the "Enter Code" message with an outline using the default font
            enter_code_text = "Enter Code"
            outline_color = (0, 0, 0)  # Black outline color
            text_color = (255, 255, 255)  # White text color

            # Render the text outline
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                outline_surface = self.font.render(enter_code_text, True, outline_color)
                screen.blit(outline_surface, (self.box_x - 25 + dx, self.box_y - 80 + dy))

            # Render the main text
            text_surface = self.font.render(enter_code_text, True, text_color)
            screen.blit(text_surface, (self.box_x - 25, self.box_y - 80))

            # Show feedback on the number of correct codes
            feedback_text = ""

            if len(self.correct_codes_entered) == 1:
                feedback_text = "One down. Two to go."
            elif len(self.correct_codes_entered) == 2:
                feedback_text = "One more left."
            elif len(self.correct_codes_entered) == 3:
                feedback_text = "All codes inserted."

            # Calculate the feedback text position (centered on the input box)
            feedback_surface = self.font.render(feedback_text, True, (255, 255, 255))

            # Calculate position for feedback text (centered on the input box, below the input box)
            feedback_x = self.box_x + (self.box_width // 2) - (feedback_surface.get_width() // 2)
            feedback_y = self.box_y + self.box_height + 10  # Just below the input box

            # Render the outline of the feedback text (to make it stand out)
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                outline_surface = self.font.render(feedback_text, True, (0, 0, 0))  # Black outline
                screen.blit(outline_surface, (feedback_x + dx, feedback_y + dy))

            # Render the actual feedback text
            screen.blit(feedback_surface, (feedback_x, feedback_y))

            # If the puzzle is solved, show a success message using the default font
            if self.solved:
                # Fill the screen with black to prepare for the success message
                screen.fill((0, 0, 0))
                pygame.display.flip()  # Update the screen to show the black screen
                pygame.time.wait(1000)  # Wait for 1 second

                # Display success message
                solved_text = self.font.render("Code Accepted! Puzzle Solved!", True, (0, 255, 0))
                screen.blit(solved_text,
                            (screen.get_width() // 2 - solved_text.get_width() // 2, screen.get_height() // 2))

                pygame.display.flip()  # Update the screen again to show the success message
                pygame.time.wait(2000)  # Wait for 2 seconds to let the player see the message

                # Mark the mini-game as completed, locking it
                self.mini_game_completed = True  # Now the mini-game is locked and cannot be played again

            # If game over (wrong code entered), reset the game
            if self.game_over:
                # Reset game state
                self.reset_game()
                # Show the "Start Over" message
                screen.fill((0, 0, 0))  # Black screen for "Start Over"
                start_over_text = self.font.render("Start Over", True, (255, 0, 0))  # Red text for "Start Over"
                screen.blit(start_over_text,
                            (screen.get_width() // 2 - start_over_text.get_width() // 2, screen.get_height() // 2))
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds before restarting the game

            # Apply brightness and sound settings dynamically
            apply_brightness_and_sound(screen)
            # Update the screen
            pygame.display.flip()
            clock.tick(60)

        return 'game'  # Return to main game after solving the mini-game
































