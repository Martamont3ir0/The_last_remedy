


from config import *
from shed import *
import pygame
from user_info import *
from powerup import *

class Chest:
    """
    The Chest class represents a container that can hold items, with functionality to add, remove,
    and describe the contents. Each chest is associated with a specific client.

    Attributes:
    - items: A list to store the items contained within the chest.
    - client: The client who owns the chest (default is "Luca Quinn").

    Methods:
    - __str__: Returns a string representation of the chest, including the client's name and the number
      of items inside the chest.
    - add_item: Adds an Item object to the chest.
    - remove_item: Removes an Item object from the chest if it exists.
    """

    def __init__(self):
        """
        Initializes the chest with an empty list of items and assigns a default client name "Luca Quinn".
        """
        self.items = []  # Initializes the chest with no items.
        self.client = "Luca Quinn"  # Sets the default client for the chest.

    def __str__(self):
        """
        Returns a string representation of the chest, including the number of items and its ownership.
        If the chest is empty, it explicitly states that.
        """
        if self.client is not None:
            info = (f"This chest belongs to {self.client}."
                    f" It is a chest with {len(self.items)} items.")
            if len(self.items) == 0:
                info += " The chest is currently empty."
            return info

    def add_item(self, item: 'Item'):
        """
        Adds an item to the chest.

        Args:
        - item: The Item object to be added to the chest.

        If the item is successfully added, it is appended to the `items` list of the chest.
        """
        self.items.append(item)  # Adds the item to the chest.

    def remove_item(self, item: 'Item'):
        """
        Removes an item from the chest if it exists.

        Args:
        - item: The Item object to be removed from the chest.

        If the item is found in the chest, it is removed from the `items` list.
        If the item is not found, a message is printed indicating its absence.
        """
        if item in self.items:
            self.items.remove(item)  # Remove the item from the chest.
            print(f"{item.name} has been removed from the chest.")  # Notify the user.
        else:
            print(f"{item.name} is not in the chest.")  # Notify the user if the item is not in the chest.


class Item:
    """
    The Item class represents an individual item with a name, value, and associated image.

    Attributes:
    - name: The name of the item (e.g., "Health Potion").
    - value: The value or significance of the item (e.g., price, power, etc.).
    - image_path: The file path of the image representing the item.

    Methods:
    - __str__: Returns a string representation of the item, showing its name, value, and image path.
    """

    def __init__(self, name, value, image_path):
        """
        Initializes an Item object with a name, value, and image path.

        Args:
        - name: The name of the item.
        - value: The value of the item (can represent the cost, worth, or power).
        - image_path: The file path to the image that represents the item.
        """
        self.name = name  # Sets the name of the item.
        self.value = value  # Sets the value of the item.
        self.image_path = image_path  # Sets the image path of the item.

    def __str__(self):
        """
        Returns a string representation of the item, showing its name, value, and image path.
        """
        return f"Item(name={self.name}, value={self.value}, image_path={self.image_path})"


# Loading and scaling assets used in the backpack and shop window
return_symbol = pygame.image.load("img/return_symbol.png")  # Loading the return symbol image
return_symbol = pygame.transform.scale(return_symbol, (90, 90))  # Resizing the return symbol image
return_symbol_rect = return_symbol.get_rect(topleft=(30, 20))  # Setting the position of the return symbol

# Creating the chest (backpack) of Luca Quinn, where items will be stored
backpack_chest = Chest()  # Creating the chest object
map_wastes = Item("Map", 0, "img/map.png")  # Creating a map item
backpack_chest.add_item(map_wastes)  # Adding the map item to the chest

# Loading background and symbols for the backpack and shop
bg_backpack = pygame.image.load("img/backpackchest.png")  # Background image for the backpack
add_symbol = pygame.image.load("img/add_symbol.png")  # Loading the add symbol image
add_symbol = pygame.transform.scale(add_symbol, (100, 100))  # Resizing the add symbol image
add_symbol_rect = add_symbol.get_rect(topleft=(600, 20))  # Setting the position for the add symbol


def shop_window(screen, player):
    """
    This function handles the shop window where the player can buy items, view their money, and interact with available items.

    Args:
        screen (pygame.Surface): The surface on which everything will be drawn (the game screen).
        player (Player): The player object representing the current player, containing their inventory and money.

    Returns:
        str: The outcome, typically "backpack", signaling the transition to the backpack screen.
    """

    # List of items available for purchase in the shop
    shop_items = [
        {"name": "Sunglasses", "value": 10, "image_path": "img/glasses.png"},
        {"name": "Laser", "value": 20, "image_path": "img/laser.png"},
        {"name": "Health Potion", "value": 30, "image_path": "img/health_potion.png"},
        {"name": "Grenade", "value": 100, "image_path": "img/grenade.png"},
        {"name": "Sadness Potion", "value": 200, "image_path": "img/sadpotion.png"},
        {"name": "Airplane", "value": 11340, "image_path": ""}
    ]

    # Loading the shop background image
    bg_shop = pygame.image.load("img/shop.png")
    running = True  # Flag to keep the shop window running

    while running:
        screen.blit(bg_shop, (0, 0))  # Rendering the shop background

        # Displaying player info in the shop (like money, health, etc.)
        user_info(player, screen, False)

        # Title of the shop
        font = pygame.font.Font(None, 26)  # Font for the shop items
        font_title = pygame.font.Font(None, 60)  # Font for the shop title
        shop_title = font_title.render("Welcome to the shop!", True, greenish)
        text_rect = shop_title.get_rect()  # Get the rectangle of the text surface

        # Center the text rectangle on the screen
        text_rect.center = (width // 2, 65)
        screen.blit(shop_title, text_rect)  # Display the title on the screen
        screen.blit(return_symbol, return_symbol_rect)  # Display the return symbol for going back to the backpack

        # Display available items for purchase
        item_rects = []  # List to store item rectangles for collision detection
        for index, item in enumerate(shop_items):
            # Display the name and value of the item
            text = font.render(f"{item['name']} - {item['value']} coins", True, deep_black)
            text_rect = text.get_rect(topleft=(80, 155 + index * 60))  # Position of the item text
            screen.blit(text, text_rect)  # Display the item text

            # Check if the player can afford the item
            if player.money >= item['value']:
                note = font.render("BUY", True, greenish)
                note_rect = note.get_rect(topleft=(620, 155 + index * 60))  # Position for the "BUY" text
            else:
                note = font.render("TOO EXPENSIVE", True, dark_red)
                note_rect = note.get_rect(topleft=(519, 155 + index * 60))  # Position for the "TOO EXPENSIVE" text
            screen.blit(note, note_rect)  # Render the note (either "BUY" or "TOO EXPENSIVE")

            item_rects.append((note_rect, item))  # Store the rectangle for collision detection

            # Apply brightness and sound settings dynamically (additional functions might be defined elsewhere)
            apply_brightness_and_sound(screen)

        pygame.display.flip()  # Update the display with all changes

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Handle quitting the game (close the window)
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                # Check if the player clicked on any shop item
                for rect, item in item_rects:
                    if rect.collidepoint(event.pos):  # If clicked within the item's rectangle
                        # Check if the player can afford the item
                        if player.money >= item['value']:
                            player.money -= item['value']  # Deduct the cost from the player's money
                            new_item = Item(item['name'], item['value'], item['image_path'])  # Create the item object
                            print(f"Remaining money: {player.money} coins")
                            backpack_chest.add_item(new_item)  # Add the item to the player's chest (backpack)
                            return "backpack"  # Return to the backpack screen

                        else:
                            # If the player doesn't have enough money, print a message
                            print("You don't have enough money")

                # Check if the return symbol was clicked
                if return_symbol_rect.collidepoint(event.pos):  # Return symbol clicked
                    return "backpack"  # Return to the backpack screen


def backpack(screen, player, level_):
    """
    Function to display and interact with the player's backpack.

    The backpack shows the items that the player has collected and allows the player to use them.
    Depending on the item clicked, it triggers specific actions or changes, such as equipping a weapon, using a potion, or returning to the shop.

    Args:
        screen (pygame.Surface): The surface on which the backpack interface will be drawn (the game screen).
        player (Player): The player object representing the current player, containing their inventory and attributes.
        level_ (int): The current game level, used to determine the appropriate level to return to after interacting with the backpack.

    Returns:
        str: The next screen or level to transition to ("shop", or the previous level such as "shed", "level3").
    """

    # Determine the level to return to based on the current level
    if level_ == 2:
        level = "shed"  # The level to return to if level_ is 2
    elif level_ == 3:
        level = "level3"  # The level to return to if level_ is 3

    # Configuration for items in the backpack with their dimensions and positions
    item_configs = {
        "Sunglasses": (200, 200, (20, 200)),  # (width, height, position)
        "Map": (190, 150, (30, 420)),
        "Laser": (180, 140, (280, 200)),
        "Health Potion": (130, 130, (550, 210)),
        "Grenade": (110, 170, (580, 370)),
        "Sadness Potion": (140, 140, (300, 400))
    }

    while True:
        # Event handling loop for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the player closes the window
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
                # Check if the add symbol is clicked to return to the shop
                if add_symbol_rect.collidepoint(event.pos):
                    return "shop"
                # Check if the return symbol is clicked to return to the previous level
                elif return_symbol_rect.collidepoint(event.pos):
                    return level

                # Check for clicks on items in the backpack
                for item in backpack_chest.items:
                    print(item)  # Print the item to see what it is
                    print(type(item))  # Print the type of the item
                    if item.name in item_configs.keys():  # Process only items that are configured
                        item_image = pygame.image.load(item.image_path)  # Load the item's image
                        width, height, position = item_configs[
                            item.name]  # Get item config for width, height, and position
                        item_image = pygame.transform.scale(item_image, (width, height))  # Scale the image to fit
                        item_rect = item_image.get_rect(topleft=position)  # Create a rectangle for the item

                        # Check if the item is clicked
                        if item_rect.collidepoint(event.pos):
                            # Handle specific item actions when clicked

                            if player.glasses_used:  # If glasses have been used, remove the item (e.g., map)
                                backpack_chest.remove_item(item)  # Remove the item from the backpack
                            if item.name == "Sunglasses":
                                player.glasses_used = True  # Mark sunglasses as used
                                backpack_chest.remove_item(item)  # Remove sunglasses from the backpack
                                return level
                            elif item.name == "Map" and player.glasses_used:  # Check if map is clicked after glasses are used
                                player.map_used = True  # Mark map as used
                                return level
                            elif item.name == "Laser":
                                player.weapon = "Laser"  # Equip the laser weapon
                                player.use_laser = True  # Enable laser use
                                return level
                            elif item.name == "Health Potion":
                                # Create a health potion and apply it to the player
                                health_potion = HealthRegeneration(100 - player.health)  # Create health potion
                                health_potion.affect_player(player, player.default_list)  # Apply the potion effect
                                return level
                            elif item.name == "Grenade":
                                player.weapon = "Grenade"  # Equip the grenade weapon
                                return level
                            elif item.name == "Sadness Potion":
                                sadness_potion = Sadness()  # Create sadness potion
                                sadness_potion.affect_player(player, player.default_list)  # Apply the potion effect
                                return level

        # Drawing the backpack interface
        screen.blit(bg_backpack, (0, 0))  # Draw the background of the backpack screen
        screen.blit(add_symbol, add_symbol_rect)  # Draw the add symbol to indicate adding items
        screen.blit(return_symbol, return_symbol_rect)  # Draw the return symbol for returning to the previous level

        # Draw each item in the backpack
        for item in backpack_chest.items:
            if isinstance(item, Item) and item.name in item_configs.keys():  # Only process items that are configured
                item_image = pygame.image.load(item.image_path)  # Load the item image
                width, height, position = item_configs[
                    item.name]  # Get the item's configuration (width, height, position)
                item_image = pygame.transform.scale(item_image, (width, height))  # Scale the image
                item_rect = item_image.get_rect(topleft=position)  # Create a rectangle for the item to detect clicks
                screen.blit(item_image, item_rect.topleft)  # Display the item image at its defined position

        # Apply brightness and sound settings dynamically (additional functions defined elsewhere)
        apply_brightness_and_sound(screen)

        pygame.display.flip()  # Update the display with all changes

