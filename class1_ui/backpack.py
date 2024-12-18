from class1_ui.shed import shed
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
        # making sure the item is an Item or None, otherwise crash the program with an explanation
        assert isinstance(item, Item) or item is None, "You're silly. The item is NOT valid"

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
return_symbol_rect = return_symbol.get_rect(topleft=(30, 610))
return_symbol_rect2 = return_symbol.get_rect(topleft=(15, 10))

def shop_window(screen,player,selected_character,bg_width):
    # Define items available in the shop
    shop_items = [
        {"name": "Sunglasses", "value": 10, "image_path": "img/glasses.png"},
        {"name": "Laser", "value": 50, "image_path": "img/laser.png"},
        {"name": "Health Potion", "value": 25, "image_path": "img/health_potion.png"},
        {"name": "Shield", "value": 40, "image_path": ""},
        {"name": "Example 1", "value": 205, "image_path": ""},
        {"name": "Grenade", "value": 10, "image_path": "img/grenade.png"}
    ]
    background = pygame.image.load("img/shop.png")
    running = True
    while running:



        screen.blit(background,(0,0))
        user_info(player, screen, False)
        #display the shop title
        font = pygame.font.Font(None, 26)
        font_title = pygame.font.Font(None, 60)
        shop_title = font_title.render("Welcome to the shop!", True, greenish)
        text_rect = shop_title.get_rect()  # Get the rectangle of the text surface

        # Center the text rectangle
        text_rect.center = (width // 2, 65)  # Center it
        screen.blit(shop_title,text_rect)
        screen.blit(return_symbol, return_symbol_rect2)

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

        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Handle quitting the game
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                for rect, item in item_rects:
                    if rect.collidepoint(event.pos):  # Check if the mouse click is within an item's rectangle
                        # Check if the player can afford the item
                        if player.money >= item['value']:
                            player.money -= item['value']  # Deduct the item's cost from the player's money
                            new_item = Item(item['name'], item['value'], item['image_path'])
                            print(f"Remaining money: {player.money} coins")
                            return new_item  # Add the item to the player's backpack

                        else:
                            # Inform the player if they don't have enough money
                            print("You don't have enough money")

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                    if return_symbol_rect2.collidepoint(event.pos):  # Check if return symbol is clicked to return
                        backpack(screen,player,selected_character,bg_width)

backpack_chest = Chest() #Create my chest as the backpack of Luca Quinn, where the player can store its things
map_wastes = Item("Map",0,"img/map.png")
backpack_chest.add_item(map_wastes)  # Add the map item to the chest

def backpack(screen,player,selected_character,bg_width):

    background = pygame.image.load("img/backpackchest.png")
    add_symbol = pygame.image.load("img/add_symbol.png")
    add_symbol = pygame.transform.scale(add_symbol, (100, 100))
    add_symbol_rect = add_symbol.get_rect(topleft=(600,600))


    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if add_symbol_rect.collidepoint(event.pos):  # Check if add symbol is clicked to enter the shop
                    new_item = shop_window(screen,player,selected_character, bg_width)
                    backpack_chest.add_item(new_item)
                    return "backpack"
                elif return_symbol_rect.collidepoint(event.pos):  # Check if return symbol is clicked to return
                    return "shed_normal"

        screen.blit(background, (0, 0))
        screen.blit(add_symbol, add_symbol_rect)
        screen.blit(return_symbol, return_symbol_rect)

        for item in backpack_chest.items:
            item_image = pygame.image.load(item.image_path)
            item_rect = None
            if item.name == "Sunglasses":
                item_image = pygame.transform.scale(item_image, (200, 200))
                item_rect = item_image.get_rect(topleft=(20, 200))  # Create a rect for the image
                # Check for mouse button down event
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                        if item_rect.collidepoint(event.pos):# Check if glasses are clicked
                            backpack_chest.remove_item(item)
                            return "shed_normal" #return to the desert and without the overlay, aka sunlight

            elif item.name == "Map":
                item_image = pygame.transform.scale(item_image, (190, 150))
                item_rect = item_image.get_rect(topleft=(30, 420))  # Create a rect for the image
                # Check for mouse button down event
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                        if item_rect.collidepoint(event.pos):  # Check if map is clicked
                            backpack_chest.remove_item(item)
                            return "shed_map"

            elif item.name == "Laser":
                item_image = pygame.transform.scale(item_image, (180, 140))
                item_rect = item_image.get_rect(topleft=(280, 200))  # Create a rect for the image
                # Check for mouse button down event
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                        if item_rect.collidepoint(event.pos):  # Check if laser is clicked
                            backpack_chest.remove_item(item)
                            player.weapon = "Laser"
                            player.use_laser= True

            elif item.name == "Health Potion":
                item_image = pygame.transform.scale(item_image, (130, 130))
                item_rect = item_image.get_rect(topleft=(550, 210))  # Create a rect for the image
                health_potion = HealthRegeneration(0,100-player.health) #Create a variable with the health regeneration powerup,where the amount is what is left for the player to be fully healthy
                # Check for mouse button down event
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                        if item_rect.collidepoint(event.pos):  # Check if potion is clicked
                            backpack_chest.remove_item(item)
                            health_potion.apply(player) #apply the power up to the player
                            return "shed_map"

            elif item.name == "Grenade":
                item_image = pygame.transform.scale(item_image, (110, 170))
                item_rect = item_image.get_rect(topleft=(580, 370))  # Create a rect for the image
                # Check for mouse button down event
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                        if item_rect.collidepoint(event.pos):  # Check if laser is clicked
                            backpack_chest.remove_item(item)
                            #player.weapon = "Grenade


            screen.blit(item_image, item_rect.topleft)  # Blit the image at the top-left of the rect

        pygame.display.flip()
