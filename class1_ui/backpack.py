from class1_ui.shed import shed
from config import *
from shed import *
import pygame


class Chest:

    def __init__(self):  # equivalent to create_chest
        # setting default values for chest
        self.items = []
        self.client = "Luca Quinn"

    def __str__(self):
        if self.client is not None:
            info = (f"This chest belongs to {self.client}."
                    f" It is a chest with {len(self.items)} items.")
            if len(self.items) == 0:
                info += " The chest is currently empty."
            return info

    def add_item(self, item: 'Item' = None, name: str = None, value: float = None, image_path: str = None):
        # making sure the item is an Item or None, otherwise crash the program with an explanation
        assert isinstance(item, Item) or item is None, "You're silly. The item is NOT valid"

        if item is None:
            # allow the user to create an item:
            assert name is not None and value is not None and image_path is not None, "Name, value, and image_path must be provided to create an item."
            item = Item(name, value, image_path)

        # adding the item to the chosen chest
        self.items.append(item)


class Item:

    def __init__(self, name, value, image_path):
        self.name = name
        self.value = value
        self.image_path = image_path

    def __str__(self):
        return f"Item(name={self.name}, value={self.value}, image_path={self.image_path})"



def backpack(screen,player,selected_character,bg_width):
    background = pygame.image.load("img/backpackchest.png")
    glasses = pygame.image.load("img/glasses.png")
    glasses = pygame.transform.scale(glasses, (200, 200))
    glasses_rect = glasses.get_rect(topleft=(80, 198))  # Create a rect for the glasses image
    while True:
        screen.blit(background, (0, 0))
        screen.blit(glasses, glasses_rect.topleft)  # Blit the image at the top-left of the rect
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # Check for mouse button down event

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if glasses_rect.collidepoint(event.pos):# Check if glasses are clicked
                    return shed(player,selected_character,bg_width,False) #return to the desert and without the overlay, aka sunlight

        pygame.display.flip()
