import pygame
import math
import level3

class InteractiveObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, activation_func=None, size=None):
        """
        Initialize an interactive object at the given position with an optional activation function and size.

        :param x: The x-coordinate for the object.
        :param y: The y-coordinate for the object.
        :param image_path: The path to the image to be used for the object.
        :param activation_func: The function to call when the object is interacted with (optional).
        :param size: The size to scale the image to (optional).
        """
        super().__init__()

        # Load the image from the provided path
        self.image = pygame.image.load(image_path)

        # Resize the image if a size is provided
        if size:
            self.image = pygame.transform.scale(self.image, size)

        # Initialize rect for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Set the object's center position to (x, y)

        # Set activation function, default to None if not provided
        self.activate_func = activation_func

    def interact(self):
        """
        Activate the interaction function if it exists. This is called when the object is interacted with.
        """
        if self.activate_func:
            self.activate_func()

    def is_near(self, player_rect, proximity):
        """
        Check if the player is within a certain proximity of the object.

        :param player_rect: The rectangle representing the player's position.
        :param proximity: The maximum allowed distance for interaction.
        :return: True if the player is close enough, False otherwise.
        """
        # Calculate Euclidean distance between the object and player
        dx = self.rect.centerx - player_rect.centerx
        dy = self.rect.centery - player_rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance <= proximity  # Return True if within proximity

    def draw(self, screen, highlight=False):
        """
        Draw the object on the screen. Optionally display the interaction prompt if the player is near.

        :param screen: The pygame screen to draw the object onto.
        :param highlight: If True, display the interaction prompt above the object.
        """
        screen.blit(self.image, self.rect)  # Draw the object image on the screen

        # If highlight is True, display the interaction prompt
        if highlight:
            font = pygame.font.Font(None, 36)  # Set font for interaction text
            interaction_prompt = font.render("Press E to interact", True, (255, 255, 255))  # Interaction prompt text

            # Position the prompt above the object
            prompt_x = self.rect.centerx - interaction_prompt.get_width() // 2
            prompt_y = self.rect.top - 30  # Fixed vertical offset

            # Draw the interaction prompt
            screen.blit(interaction_prompt, (prompt_x, prompt_y))



class ImageObject(InteractiveObject):
    def __init__(self, x, y, image_path, activation_func=None, size=None):
        """
        Initialize an ImageObject which is a simple interactive object with an image.
        Inherits from InteractiveObject.

        :param x: The x-coordinate for the object.
        :param y: The y-coordinate for the object.
        :param image_path: The path to the image for the object.
        :param activation_func: Optional activation function to run when interacting with the object.
        :param size: Optional size to scale the image.
        """
        super().__init__(x, y, image_path, activation_func, size)

    def update(self, dt):
        """
        Placeholder update method.

        :param dt: Delta time, the time difference between frames (not used for now).
        """
        pass






