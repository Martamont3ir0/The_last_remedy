


from config import *
from shed import *
import pygame
from user_info import *
from powerup import *

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

    def add_item(self, item: 'Item'):


        # adding the item to the chosen chest
        self.items.append(item)

    def remove_item(self, item: 'Item'):
        # Check if the item exists in the chest
        if item in self.items:
            self.items.remove(item)  # Remove the item
            print(f"{item.name} has been removed from the chest.")
        else:
            print(f"{item.name} is not in the chest.")


class Item:

    def __init__(self, name, value, image_path):
        self.name = name
        self.value = value
        self.image_path = image_path

    def __str__(self):
        return f"Item(name={self.name}, value={self.value}, image_path={self.image_path})"

return_symbol = pygame.image.load("img/return_symbol.png")
return_symbol = pygame.transform.scale(return_symbol, (90, 90))
return_symbol_rect = return_symbol.get_rect(topleft=(30, 20))
backpack_chest = Chest() #Create my chest as the backpack of Luca Quinn, where the player can store its things
map_wastes = Item("Map",0,"img/map.png")
backpack_chest.add_item(map_wastes)  # Add the map item to the chest
bg_backpack = pygame.image.load("img/backpackchest.png")
add_symbol = pygame.image.load("img/add_symbol.png")
add_symbol = pygame.transform.scale(add_symbol, (100, 100))
add_symbol_rect = add_symbol.get_rect(topleft=(600, 20))

def shop_window(screen,player):
    # Define items available in the shop
    shop_items = [
        {"name": "Sunglasses", "value": 10, "image_path": "img/glasses.png"},
        {"name": "Laser", "value": 50, "image_path": "img/laser.png"},
        {"name": "Health Potion", "value": 25, "image_path": "img/health_potion.png"},
        {"name": "Grenade", "value": 100, "image_path": "img/grenade.png"},
        {"name": "Airplane", "value": 9800, "image_path": ""},
        {"name": "Ship", "value": 11340, "image_path": ""}
    ]
    bg_shop = pygame.image.load("img/shop.png")
    running = True
    while running:

        screen.blit(bg_shop,(0,0))

        user_info(player, screen, False)
        #display the shop title
        font = pygame.font.Font(None, 26)
        font_title = pygame.font.Font(None, 60)
        shop_title = font_title.render("Welcome to the shop!", True, greenish)
        text_rect = shop_title.get_rect()  # Get the rectangle of the text surface

        # Center the text rectangle
        text_rect.center = (width // 2, 65)  # Center it
        screen.blit(shop_title,text_rect)
        screen.blit(return_symbol, return_symbol_rect)

        # Display the shop items
        item_rects = []  # Store the rectangles for each item for collision detection
        for index, item in enumerate(shop_items):
            text = font.render(f"{item['name']} - {item['value']} coins", True, deep_black)
            text_rect = text.get_rect(topleft=(80, 155 + index * 60))  # Position the text
            screen.blit(text, text_rect)  # Render the text onto the screen

            # Check if the player can afford the item
            if player.money >= item['value']:
                note = font.render("BUY", True, greenish)
                note_rect = note.get_rect(topleft=(620, 155 + index * 60))  # Position the text
            else:
                note = font.render("TOO EXPENSIVE", True, dark_red)
                note_rect = note.get_rect(topleft=(519, 155 + index * 60))  # Position the text
            screen.blit(note, note_rect)  # Render the text onto the screen

            item_rects.append((note_rect, item))

            # Apply brightness and sound settings dynamically
            apply_brightness_and_sound(screen)

        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Handle quitting the game
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                for rect, item in item_rects:
                    if rect.collidepoint(event.pos):  # Check if the mouse click is within an item's rectangle
                        # Check if the player can afford the item
                        if player.money >= item['value']:
                            player.money -= item['value']  # Deduct the item's cost from the player's money
                            new_item = Item(item['name'], item['value'], item['image_path'])
                            print(f"Remaining money: {player.money} coins")
                            backpack_chest.add_item(new_item)  # Add new item to the backpack
                            return "backpack"

                        else:
                            # Inform the player if they don't have enough money
                            print("You don't have enough money")


                if return_symbol_rect.collidepoint(event.pos):  # Check if return symbol is clicked to return
                    return "backpack"

def backpack(screen, player):

    # Configuration for items in the backpack
    item_configs = {
        "Sunglasses": (200, 200, (20, 200)),  # (width, height, position)
        "Map": (190, 150, (30, 420)),
        "Laser": (180, 140, (280, 200)),
        "Health Potion": (130, 130, (550, 210)),
        "Grenade": (110, 170, (580, 370)),
    }

    while True:
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle window close event
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
                # Check if the add symbol is clicked
                if add_symbol_rect.collidepoint(event.pos):
                    return "shop"
                # Check if the return symbol is clicked
                elif return_symbol_rect.collidepoint(event.pos):
                    return "shed"

                # Check for item clicks in the backpack
                for item in backpack_chest.items:
                    print(item)  # Print the item to see what it is
                    print(type(item))  # Print the type of the item
                    if item.name in item_configs.keys():  # Only process items that are configured
                        item_image = pygame.image.load(item.image_path)  # Load the item's image
                        width, height, position = item_configs[item.name]  # Get item config
                        item_image = pygame.transform.scale(item_image, (width, height))  # Scale the image
                        item_rect = item_image.get_rect(topleft=position)  # Create a rect for the item

                        # Check if the item is clicked
                        if item_rect.collidepoint(event.pos):
                            if player.glasses_used: #in case map is clicked and glasses haven't been used
                                backpack_chest.remove_item(item)  # Remove the item from the backpack
                            # Handle item-specific actions
                            if item.name == "Sunglasses":
                                player.glasses_used = True
                                backpack_chest.remove_item(item)  # Remove glasses from the backpack since they were not removed above
                                return "shed"
                            elif item.name == "Map" and player.glasses_used:
                                player.map_used = True
                                return "shed"
                            elif item.name == "Laser":
                                player.weapon = "Laser"  # Equip the laser weapon
                                player.use_laser = True
                                return "shed"
                            elif item.name == "Health Potion":
                                health_potion = HealthRegeneration(0, 100 - player.health)  # Create health potion
                                health_potion.apply(player)  # Apply health potion effect
                                return "shed"
                            elif item.name == "Grenade":
                                player.weapon = "Grenade"  # Equip the grenade weapon
                                return "shed"

        # Drawing the backpack interface
        screen.blit(bg_backpack, (0, 0))  # Draw the background
        screen.blit(add_symbol, add_symbol_rect)  # Draw the add symbol
        screen.blit(return_symbol, return_symbol_rect)  # Draw the return symbol


        # Draw each item in the backpack

        for item in backpack_chest.items:
            if isinstance(item, Item) and item.name in item_configs.keys():  # Only process items that are configured
                item_image = pygame.image.load(item.image_path)  # Load the item's image
                width, height, position = item_configs[item.name]  # Get item config
                item_image = pygame.transform.scale(item_image, (width, height))  # Scale the image
                item_rect = item_image.get_rect(topleft=position)  # Create a rect for the item
                screen.blit(item_image, item_rect.topleft)  # Blit the item image at its position

        # Apply brightness and sound settings dynamically
        apply_brightness_and_sound(screen)

        pygame.display.flip()  # Update the display