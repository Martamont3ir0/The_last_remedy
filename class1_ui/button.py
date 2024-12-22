import pygame
from interactive_object import InteractiveObject


class Button(InteractiveObject):
    def __init__(self):

        image_path = "img/button.png"
        super().__init__(600, 370, image_path, self.activate, size=(250, 300))
        self.code = ""

    def enter_code(self, digit):
        """Enter a digit into the code input."""
        self.code += digit

    def activate(self):
        """Activate the button after the correct code is entered."""
        if self.code == "1626":  # Example code
            print("Button activated!")
            # Your button activation code goes here (e.g., trigger puzzle solution)

    def draw(self, screen, highlight=False):
        """Draw the button, optionally with highlight."""
        super().draw(screen)  # Call the parent class's draw method

        # If the player is close enough, show the interaction prompt
        if highlight:
            font = pygame.font.Font(None, 36)
            interaction_prompt = font.render("Press E to interact", True, (255, 255, 255))  # White text

            # Create a black outline effect by drawing the text multiple times with slight offsets
            outline_color = (0, 0, 0)  # Black outline color
            outline_offset = 2  # Offset for outline around the text

            # Draw the outline (black) in all directions
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

            # Draw the main (white) text
            screen.blit(interaction_prompt,
                        (self.rect.centerx - interaction_prompt.get_width() // 2, self.rect.top - 30))








