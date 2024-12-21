import pygame
from interactive_object import InteractiveObject


class ElixirVessel(InteractiveObject):
    def __init__(self, x, y):
        # Define the activate method before calling the parent constructor
        def activate():
            """Check if the ingredients match the requirements to create the Elixir."""
            if all(ingredient in self.inventory for ingredient in self.ingredients):
                self.is_solved = True
                print("Elixir created! The fate of humanity is now in your hands.")
            else:
                print("The Elixir is incomplete! Add the correct ingredients.")

        # Path to the Elixir vessel image
        image_path = "img/elixir_vessel.png"

        # Call the parent constructor with the activation method
        super().__init__(x, y, image_path, activate, size=(332, 284))  # Resize the image

        # Puzzle state and ingredients
        self.is_solved = False
        self.ingredients = ["Solanum", "Elixir"]  # Correct ingredients for the Elixir
        self.inventory = []  # Store ingredients that the player has added

        self.rect.x -= 50
        self.rect.y = 200

    def add_ingredient(self, ingredient):
        """Allow the player to add an ingredient to the Elixir vessel."""
        if ingredient not in self.inventory:
            self.inventory.append(ingredient)
            print(f"{ingredient} added to the vessel.")
        else:
            print(f"{ingredient} is already in the vessel.")

    def is_puzzle_solved(self):
        """Return whether the Elixir puzzle is solved."""
        return self.is_solved

    def draw(self, screen, highlight=False):
        """Draw the Elixir vessel with the interaction prompt and black outline around the text."""
        super().draw(screen)  # Draw the Elixir vessel image

        # If the player is near the Elixir vessel, show the "Press E to interact" prompt
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








