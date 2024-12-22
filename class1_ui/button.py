import pygame
from interactive_object import InteractiveObject


class Button(InteractiveObject):
    """
    Represents a button that can be interacted with in the game.

    The button can be activated by entering a specific code and provides visual feedback when the player is nearby.

    Attributes:
        code (str): The code entered by the player to activate the button. Initially, it is an empty string.
    """

    def __init__(self):
        """
        Initializes a new Button instance.

        The button image is loaded, and the button's position and activation function are set.
        The default code is an empty string.
        """
        image_path = "img/button.png"  # Path to the button image
        super().__init__(600, 370, image_path, self.activate,
                         size=(250, 300))  # Initialize the base class with position, image, and activation function
        self.code = ""  # The code entered by the player (initially empty)

    def enter_code(self, digit):
        """
        Enter a digit into the code input.

        Args:
            digit (str): A single digit to add to the current code entered.
        """
        self.code += digit  # Append the entered digit to the code

    def activate(self):
        """
        Activate the button after the correct code is entered.

        If the entered code matches the correct code (e.g., "1626"), the button is activated.
        You can add more functionality for the button's activation here, such as triggering a puzzle solution.
        """
        if self.code == "1626":  # Check if the entered code matches the correct one
            print("Button activated!")  # Placeholder for button activation, e.g., solving a puzzle or opening a door
            # Add further functionality for the button activation here, such as triggering game events

    def draw(self, screen, highlight=False):
        """
        Draw the button on the screen, optionally highlighting it to show an interaction prompt.

        Args:
            screen (pygame.Surface): The screen to draw the button onto.
            highlight (bool): If True, draw a highlight and interaction prompt for the button.
        """
        super().draw(screen)  # Call the parent class's draw method to render the button

        # If the player is close enough to interact with the button, show the interaction prompt
        if highlight:
            font = pygame.font.Font(None, 36)  # Font for the interaction prompt
            interaction_prompt = font.render("Press E to interact", True, (255, 255, 255))  # White text

            # Create a black outline effect for the interaction text by drawing it multiple times with slight offsets
            outline_color = (0, 0, 0)  # Black outline color
            outline_offset = 2  # Offset for the outline around the text

            # Draw the outline in all directions (to simulate a glow or shadow effect)
            screen.blit(font.render("Press E to interact", True, outline_color), (
                self.rect.centerx - interaction_prompt.get_width() // 2 - outline_offset,
                self.rect.top - 30 - outline_offset))
            screen.blit(font.render("Press E to interact", True, outline_color), (
                self.rect.centerx - interaction_prompt.get_width() // 2 + outline_offset,
                self.rect.top - 30 - outline_offset))
            screen.blit(font.render("Press E to interact", True, outline_color), (
                self.rect.centerx - interaction_prompt.get_width() // 2 - outline_offset,
                self.rect.top - 30 + outline_offset))
            screen.blit(font.render("Press E to interact", True, outline_color), (
                self.rect.centerx - interaction_prompt.get_width() // 2 + outline_offset,
                self.rect.top - 30 + outline_offset))

            # Draw the main interaction prompt (white text)
            screen.blit(interaction_prompt,
                        (self.rect.centerx - interaction_prompt.get_width() // 2, self.rect.top - 30))







