import pygame
import math
import level3

class InteractiveObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, activation_func=None, size=None):
        super().__init__()

        # Load the image
        self.image = pygame.image.load(image_path)

        # Resize the image if a size is provided
        if size:
            self.image = pygame.transform.scale(self.image, size)

        # Initialize rect for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Set activation function (default to None if not provided)
        self.activate_func = activation_func

    def interact(self):
        """Activate the interaction if the activation function exists."""
        if self.activate_func:
            self.activate_func()

    def is_near(self, player_rect, proximity=40):
        """Check if the player is within a certain distance (proximity)."""
        # Calculate Euclidean distance between object and player
        dx = self.rect.centerx - player_rect.centerx
        dy = self.rect.centery - player_rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance <= proximity  # If within the proximity, return True

    def draw(self, screen, highlight=False):
        """Draw the object on the screen and optionally display the interaction prompt."""
        screen.blit(self.image, self.rect)

        if highlight:
            # Set the font for the interaction text
            font = pygame.font.Font(None, 36)

            # Create the interaction prompt text
            interaction_prompt = font.render("Press E to interact", True, (255, 255, 255))

            # Position the prompt directly above the object
            prompt_x = self.rect.centerx - interaction_prompt.get_width() // 2
            prompt_y = self.rect.top - 30  # Adjust vertical position (fixed offset)

            # Blit the text to the screen
            screen.blit(interaction_prompt, (prompt_x, prompt_y))


class ImageObject(InteractiveObject):
    def __init__(self, x, y, image_path, activation_func=None, size=None):
        """Initialize the ImageObject as a standard InteractiveObject."""
        super().__init__(x, y, image_path, activation_func, size)

    def update(self, dt):
        """Placeholder method for updates, does nothing for now."""
        pass





