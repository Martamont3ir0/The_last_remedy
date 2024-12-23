
# Config file for global constants and settings
import pygame


def apply_brightness_and_sound(screen):
    """
    Apply the current brightness and sound settings globally.

    This function adjusts the screen brightness by overlaying a transparent
    surface with varying opacity and also adjusts the sound volume of the game.

    Args:
        screen (pygame.Surface): The Pygame screen where the brightness overlay
                                  will be applied.
    """

    # Apply brightness overlay
    brightness_value = game_settings.get("brightness",
                                         1.0)  # Retrieve the brightness setting (default is 1.0 for full brightness)

    # Create an overlay surface that matches the screen resolution and supports transparency
    brightness_overlay = pygame.Surface(resolution, pygame.SRCALPHA)

    # Calculate the alpha value based on the brightness setting (darker means lower brightness)
    brightness_alpha = int((1 - brightness_value) * 255)  # Inverse of brightness, 0 is fully bright, 255 is fully dim

    # Fill the overlay with black color and adjust its transparency based on the brightness
    brightness_overlay.fill((0, 0, 0, brightness_alpha))  # Apply transparency (alpha) to darken the screen
    screen.blit(brightness_overlay, (0, 0))  # Blit (draw) the brightness overlay on the screen

    # Apply sound volume setting
    sound_volume = game_settings.get("sound_volume", 0.5)  # Retrieve the sound volume setting (default is 0.5 for 50%)
    pygame.mixer.music.set_volume(sound_volume)  # Set the global music volume in the mixer to the desired level


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

