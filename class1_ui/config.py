  # Config file for global constants and settings

import json
import pygame


def save_settings(filename="settings.json"):
    with open(filename, "w") as file:
        json.dump(game_settings, file)

def load_settings(filename="settings.json"):
    global game_settings
    try:
        with open(filename, "r") as file:
            game_settings.update(json.load(file))
    except FileNotFoundError:
        pass  # Use default settings if no file is found

def apply_brightness_and_sound(screen):
    """
    Apply the current brightness and sound settings globally.
    """
    # Apply brightness overlay
    brightness_value = game_settings.get("brightness", 1.0)  # Default to full brightness if not set
    brightness_overlay = pygame.Surface(resolution, pygame.SRCALPHA)
    brightness_alpha = int((1 - brightness_value) * 255)  # Calculate alpha value
    brightness_overlay.fill((0, 0, 0, brightness_alpha))  # Apply brightness dimming
    screen.blit(brightness_overlay, (0, 0))

    # Apply sound volume
    pygame.mixer.music.set_volume(game_settings.get("sound_volume", 0.5))  # Default to 50% if not set


# COLORS
dark_red = (138, 0, 0)          # Dark red for buttons
deep_black = (19, 20, 20)       # Almost black for background
grey = (59, 60, 60)             # Dark grey for alternate buttons
white = (254, 255, 255)         # White for readable text
glowing_light_red = (239, 128, 128)  # Light red for brighter text
blue = (0, 0, 255)              # Blue color
green = (34, 139, 34)           # Green color
yellow = (255, 255, 0)          # Yellow color
red = (150, 0, 24)              # Red color
cute_purple = (128, 0, 128)     # Purple color
greenish = (182, 215, 168)      # Greenish tint

# SCREEN SETTINGS
resolution = (720, 720)         # Screen resolution (width, height)
width, height = resolution      # Width and height extracted from resolution
fps = 60                        # Frames per second

# ENTITY SIZES
player_size = (50, 100)         # Player size (width, height)
enemy_size = (40, 40)           # Enemy size (width, height)
bullet_size = 7                 # Bullet size (diameter)

# FILE PATHS
# These are used to centralize the paths for all assets
audio_files = {
    "background_music": "audio/Star Wars IV A new hope - Binary Sunset (Force Theme).mp3",
}

image_files = {
    "main_background": "img/main_background_screen.jpg",
    "credits_background": "img/creditsbg.png",
    "rules_background": "img/backgroundstory.jpg",
}

# FONT SETTINGS
fonts = {
    "bookantiqua": ("bookantiqua", 40),
    "title_font": ("garamond", 80, True, True),  # Bold, Italic
    "start_game_font": ("perpetua", 50),
    "dialog_font": ("timesnewroman", 25),
    "header_font": ("timesnewroman", 50, True),  # Bold
}

# BUTTON SETTINGS
button_settings = {
    "default_width": 180,
    "default_height": 60,
    "default_border_radius": 10,
    "default_padding": (20, 10),
}

#puzzle configuration
#red, green, blue, yellow, cyan,magenta, orange
puzzle_colors=[
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (255,165,0)
]

#wire starting positions: left side
puzzle_wire_positions=[
    (100, 200), (100, 280), (100, 360),
    (100, 440), (100, 520), (100, 600), (100, 680)
]

#node positions:right side
puzzle_node_positions=[
    (600, 200), (600, 280), (600, 360),
    (600, 440), (600, 520), (600, 600), (600, 680)
]

game_settings={
    "brightness": 1.0, #default brightness
    "sound_volume": 0.5 #default sound volume
}
