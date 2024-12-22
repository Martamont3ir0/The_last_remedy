import pygame
from interactive_object import InteractiveObject


class ElixirVessel(InteractiveObject):
    def __init__(self):
        """
        Initialize the ElixirVessel object, calling the parent constructor and setting up
        the vessel's properties like image, ingredients, and inventory.
        """
        # Call the parent constructor with the activation method
        super().__init__(360, 350, "img/elixir_vessel.png", self.activate, size=(332, 284))  # Resize the image

        # Puzzle state and ingredients
        self.is_solved = False  # Track if the puzzle has been solved
        self.ingredients = ["Solanum", "Elixir"]  # The required ingredients for the Elixir
        self.inventory = []  # Store ingredients that the player has added

    def activate(self):
        """
        Check if the ingredients match the requirements to create the Elixir.
        If the ingredients are correct, mark the puzzle as solved.
        """
        if all(ingredient in self.inventory for ingredient in self.ingredients):
            self.is_solved = True  # Elixir is created
            print("Elixir created! The fate of humanity is now in your hands.")
        else:
            print("The Elixir is incomplete! Add the correct ingredients.")  # Puzzle not solved

    def add_ingredient(self, ingredient):
        """
        Allow the player to add an ingredient to the Elixir vessel.
        If the ingredient is already in the vessel, it is not added again.
        """
        if ingredient not in self.inventory:
            self.inventory.append(ingredient)  # Add the ingredient if it's not already in the inventory
            print(f"{ingredient} added to the vessel.")
        else:
            print(f"{ingredient} is already in the vessel.")  # Inform the player if the ingredient is a duplicate

    def is_puzzle_solved(self):
        """
        Return whether the Elixir puzzle is solved.
        """
        return self.is_solved  # Return the current solved state of the puzzle

    def draw(self, screen, highlight=False):
        """
        Draw the Elixir vessel image and the interaction prompt.
        If the player is near the vessel, show the "Press E to interact" prompt with an outline effect.
        """
        super().draw(screen)  # Draw the Elixir vessel image from the parent class

        # If the player is near the Elixir vessel, show the "Press E to interact" prompt
        if highlight:
            font = pygame.font.Font(None, 36)  # Font for the interaction prompt
            interaction_prompt = font.render("Press E to interact", True, (255, 255, 255))  # White text for prompt

            # Create a black outline effect by drawing the text multiple times with slight offsets
            outline_color = (0, 0, 0)  # Black outline color
            outline_offset = 2  # Offset for outline around the text

            # Draw the outline (black) in all directions to create the effect
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

            # Draw the main (white) text on top of the outline
            screen.blit(interaction_prompt,
                        (self.rect.centerx - interaction_prompt.get_width() // 2, self.rect.top - 30))







