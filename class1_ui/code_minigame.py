import pygame
from config import *


class CodeEntryMiniGame:
    """
    Represents a mini-game where the player needs to enter a correct code to proceed.

    The game displays a notebook image with a riddle, and the player must input a valid code to solve the puzzle.
    After solving the puzzle, a confirmation message is shown, and the game progresses.

    Attributes:
        background (pygame.Surface): Background image for the mini-game.
        notebook_image (pygame.Surface): Scaled image of a notebook to display in the mini-game.
        valid_codes (list): A list of valid codes that can solve the puzzle.
        input_text (str): The current input text entered by the player.
        solved (bool): Whether the puzzle has been solved.
        active (bool): Whether the input box is active for text input.
        correct_codes_entered (list): List of valid codes entered by the player.
        game_over (bool): Flag indicating whether the game is over.
        mini_game_completed (bool): Flag indicating whether the mini-game has been solved and locked.
    """

    def __init__(self, background_path, notebook_image_path, valid_codes):
        """
        Initializes the CodeEntryMiniGame instance with the given parameters.

        Args:
            background_path (str): The file path to the background image.
            notebook_image_path (str): The file path to the notebook image.
            valid_codes (list): List of valid codes that the player can enter to solve the puzzle.
        """
        # Load the background image
        self.background = pygame.image.load(background_path)

        # Load and scale the notebook image to be wider
        original_notebook_image = pygame.image.load(notebook_image_path)
        self.notebook_image = pygame.transform.scale(original_notebook_image, (475, 200))  # Wider notebook

        self.valid_codes = valid_codes  # List of valid codes for the mini-game
        self.input_text = ""  # Code being typed by the player

        # Load custom handwritten fonts for the riddle text
        try:
            self.handwritten_font = pygame.font.Font("fonts/handwritten_font.ttf", 28)  # Slightly larger font size
        except FileNotFoundError:
            print("Font file not found. Please make sure 'handwritten_font.ttf' is in the correct directory.")
            self.handwritten_font = pygame.font.Font(None, 28)  # Default font if custom font is missing
        except Exception as e:
            print(f"Error loading fonts: {e}")
            self.handwritten_font = pygame.font.Font(None, 28)  # Default font in case of any error

        # Main and small font for game text and UI text
        self.font = pygame.font.Font(None, 48)  # Main font
        self.small_font = pygame.font.Font(None, 32)  # Smaller font for UI feedback text

        # Input box settings
        self.box_width = 125
        self.box_height = 50
        self.box_x = 300  # Position of the input box
        self.box_y = 300  # Position of the input box

        # Other variables
        self.solved = False  # Flag to track if the puzzle is solved
        self.active = False  # Flag to track if the input box is active
        self.correct_codes_entered = []  # List to track entered valid codes (distinct)
        self.game_over = False  # Flag to track if the game is over

        # Flag to track if the mini-game has been solved and locked
        self.mini_game_completed = False  # Prevent re-playing the mini-game once solved

    def reset_game(self):
        """
        Resets the mini-game to its initial state.
        Clears entered codes, resets flags, and clears the input text.
        """
        self.correct_codes_entered = []  # Clear entered codes
        self.solved = False  # Reset puzzle solved flag
        self.game_over = False  # Reset game over flag
        self.input_text = ""  # Clear input text
        self.active = False  # Deactivate input box

    def run(self, screen, clock):
        """
        Runs the code entry mini-game. Handles input, drawing, and game flow.

        Args:
            screen (pygame.Surface): The screen to draw the mini-game on.
            clock (pygame.time.Clock): The clock used to manage frame rate.
        """
        running = True
        while running:
            # If the mini-game is completed, prevent interaction and show the solved screen
            if self.mini_game_completed:
                screen.fill((0, 0, 0))  # Fill screen with black for "Code Corrected" screen
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

            # Display the riddle text on the notebook using the handwritten fonts
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

            # Draw the input box using the default fonts
            pygame.draw.rect(screen, box_color, (self.box_x, self.box_y, self.box_width, self.box_height), 2)
            input_surface = self.font.render(self.input_text, True, (255, 255, 255))  # Render the input text
            screen.blit(input_surface, (self.box_x + 10, self.box_y + 10))  # Display the text inside the box

            # Check for player input if the box is active and mini-game is not completed
            for event in pygame.event.get():
                # Exit the game if the quit event is triggered (e.g., close window)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Check if a key is pressed while the input box is active
                if event.type == pygame.KEYDOWN and self.active:  # Only accept input if box is active
                    # Handle backspace to delete the last entered character
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]  # Remove last character from input_text
                    # Handle enter key to submit the entered code
                    elif event.key == pygame.K_RETURN:
                        # Check if the input code is valid and hasn't been entered before
                        if self.input_text in self.valid_codes and self.input_text not in self.correct_codes_entered:
                            # Add the correct code to the list of entered codes
                            self.correct_codes_entered.append(self.input_text)
                            # Check if all required codes have been entered
                            if len(self.correct_codes_entered) == len(self.valid_codes):
                                self.solved = True  # Puzzle solved after entering all valid codes
                                pygame.time.wait(1000)  # Brief pause before showing success message
                            self.input_text = ""  # Reset the text box for the next input
                        else:
                            # Inform the player if the entered code is incorrect or already entered
                            print("Incorrect code entered or already entered!")
                            self.game_over = True  # Trigger game over state

                    # Handle numeric keys (0-9) for entering the code
                    elif event.key in range(pygame.K_0, pygame.K_9 + 1):
                        # Limit the input to 4 characters
                        if len(self.input_text) < 4:
                            # Add the digit pressed to the input text
                            self.input_text += chr(event.key)

                            # Display the "Enter Code" message with an outline using the default fonts
            enter_code_text = "Enter Code"
            outline_color = (0, 0, 0)  # Black color for text outline
            text_color = (255, 255, 255)  # White color for the main text

            # Render the text outline by drawing it multiple times with slight offsets to create the outline effect
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                outline_surface = self.font.render(enter_code_text, True, outline_color)
                # Draw the outlined text at different positions to create the outline effect
                screen.blit(outline_surface, (self.box_x - 25 + dx, self.box_y - 80 + dy))

            # Render the main "Enter Code" text
            text_surface = self.font.render(enter_code_text, True, text_color)
            # Draw the main text over the outline
            screen.blit(text_surface, (self.box_x - 25, self.box_y - 80))

            # Provide feedback based on how many codes have been entered correctly
            feedback_text = ""

            # If 1 code has been entered correctly, show "One down. Two to go."
            if len(self.correct_codes_entered) == 1:
                feedback_text = "One down. Two to go."
            # If 2 codes have been entered correctly, show "One more left."
            elif len(self.correct_codes_entered) == 2:
                feedback_text = "One more left."
            # If all 3 codes have been entered correctly, show "All codes inserted."
            elif len(self.correct_codes_entered) == 3:
                feedback_text = "All codes inserted."

                # Calculate the feedback text position (centered on the input box)
                feedback_surface = self.font.render(feedback_text, True,
                                                    (255, 255, 255))  # Render the feedback text in white

                # Calculate position for feedback text (centered on the input box, below the input box)
                feedback_x = self.box_x + (self.box_width // 2) - (
                            feedback_surface.get_width() // 2)  # Center the feedback text horizontally
                feedback_y = self.box_y + self.box_height + 10  # Position the feedback text just below the input box

                # Render the outline of the feedback text (to make it stand out)
                for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    outline_surface = self.font.render(feedback_text, True, (0, 0, 0))  # Black outline
                    # Blit (draw) the outline text at positions with slight offsets
                    screen.blit(outline_surface, (feedback_x + dx, feedback_y + dy))

                # Render the actual feedback text
                screen.blit(feedback_surface, (feedback_x, feedback_y))

                # If the puzzle is solved, show a success message using the default fonts
                if self.solved:
                    # Fill the screen with black to prepare for the success message
                    screen.fill((0, 0, 0))
                    pygame.display.flip()  # Update the screen to show the black screen
                    pygame.time.wait(1000)  # Wait for 1 second to give a brief moment before success message

                    # Display success message ("Code Accepted! Puzzle Solved!")
                    solved_text = self.font.render("Code Accepted! Puzzle Solved!", True, (0, 255, 0))  # Green text
                    # Center the success message on the screen
                    screen.blit(solved_text,
                                (screen.get_width() // 2 - solved_text.get_width() // 2, screen.get_height() // 2))

                    pygame.display.flip()  # Update the screen again to show the success message
                    pygame.time.wait(2000)  # Wait for 2 seconds so the player can see the success message

                    # Mark the mini-game as completed, locking it
                    self.mini_game_completed = True  # Now the mini-game is locked and cannot be played again

                # If game over (wrong code entered), reset the game
                if self.game_over:
                    # Reset game state to start over
                    self.reset_game()
                    # Show the "Start Over" message
                    screen.fill((0, 0, 0))  # Black screen for "Start Over"
                    start_over_text = self.font.render("Start Over", True, (255, 0, 0))  # Red text for "Start Over"
                    # Center the "Start Over" message on the screen
                    screen.blit(start_over_text,
                                (screen.get_width() // 2 - start_over_text.get_width() // 2, screen.get_height() // 2))
                    pygame.display.flip()  # Update the screen
                    pygame.time.wait(2000)  # Wait for 2 seconds before restarting the game

                # Apply brightness and sound settings dynamically
                apply_brightness_and_sound(screen)  # Apply any settings like brightness or sound effects

                # Update the screen to reflect all changes
                pygame.display.flip()
                clock.tick(60)  # Set the frame rate to 60 FPS

            return 'game'  # Return to main game after solving the mini-game
































