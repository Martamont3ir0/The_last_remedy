from abc import ABC, abstractmethod
import time
import pygame
from config import *


class PowerUp(ABC):
    @abstractmethod
    def affect_player(self, player,enemies):
        """
        Apply the power-up effect to the player.
        """
        pass

    @abstractmethod
    def affect_game(self, enemies):
        """
        Affect the game or other characters in it.
        """
        pass

    @abstractmethod
    def remove(self, player, enemies):
        """
        Remove the power-up effect from the player.
        """
        pass




class DeSpawner(PowerUp):

    def __init__(self, duration):
        super().__init__()
        self._duration = duration
        self._is_active = False

    def affect_player(self, player,enemies):

        player.pup = "De-spawner"  # Set the player's current power-up
        player.shadow_color = greenish
        player.feelings = "lonely"
        self.affect_game(enemies)

    def affect_game(self, enemies):

        if enemies:  # Check if there are still enemies left
            enemy = enemies.sprites()[-1]  # Get the last enemy in the group
            #enemy.kill() #kill it

        for enemy in enemies:
            print(f"Before: {enemy.spawn_frequency}")  # Debugging line
            enemy.spawn_frequency += 6
            print(f"After: {enemy.spawn_frequency}")  # Debugging line

        print(f"DeSpawner applied.")

    def remove(self, player,enemies):
        for enemy in enemies:
            enemy.spawn_frequency -= 6
        player.pup = None  # Clear the power-up from the player
        player.shadow_color = (0,0,0,0)
        self._is_active = False
        print("DeSpawner removed.")



class SpeedBoost(PowerUp):

    def __init__(self, duration):
        super().__init__()
        self._duration = duration
        self._is_active = False

    def affect_player(self, player,enemies):

        player.speed += 8  # Increase the speed by 8
        player.pup = "SpeedBoost"  # Set the player's current power-up
        player.shadow_color = cute_purple
        player.feelings = "like a SuperHero"
        self.affect_game(enemies)

    def affect_game(self, enemies):
        print(f"SpeedBoost applied.")

    def remove(self, player, enemies):

        player.speed -= 8  # Revert effect
        player.pup = None  # Clear the power-up from the player
        player.shadow_color = (0, 0, 0, 0)
        self._is_active = False
        print("SpeedBoost removed.")


class Invincibility(PowerUp):
    def __init__(self, duration):
        super().__init__()
        self._duration = duration
        self._is_active = False


    def affect_player(self, player,enemies):
        player.is_invincible = True
        self._is_active = True
        player.shadow_color = blue
        player.pup = "Invincibility"
        player.feelings = "like Captain America"
        self.affect_game(enemies)

    def affect_game(self, enemies):
        print("Shield applied.")
    def remove(self, player,enemies):
        player.is_invincible = False
        player.shadow_color = (0, 0, 0, 0)
        player.pup = None
        self._is_active = False

        print("Shield removed.")

class HealthRegeneration(PowerUp):
    def __init__(self, regeneration_amount):
        super().__init__()
        self._regeneration_amount = regeneration_amount
        self._is_active = False

    def affect_player(self, player,enemies):
        self._is_active = True
        player.health += self._regeneration_amount  # Apply the regeneration immediately
        player.health = min(player.health, 100)  # Cap health at max (e.g., 100)
        player.pup = "Health Regeneration"
        player.shadow_color = (white)
        player.feelings = "refreshed"
        self.affect_game(enemies)
        self.remove(player,enemies) #powerup with applied instantly so the player visual characteristics are removed in the moment
    def affect_game(self, enemies):
        print("Health applied.")
    def remove(self, player,enemies):
        player.shadow_color = (0, 0, 0, 0)
        self._is_active = False
        player.pup = None

class Sadness(PowerUp):
    def __init__(self):
        super().__init__()
        self._is_active = False

    def affect_player(self, player,enemies):
        self._is_active = True
        player.feelings = "EXTRA Sad"
        player.shadow_color = (glowing_light_red)
        player.pup = "Sadness"
        self.affect_game(enemies)
        self.remove(player, enemies) #powerup with applied instantly so the player visual characteristics are removed in the moment
    def affect_game(self, enemies):
        print("Sadness applied.")

    def remove(self, player,enemies):
        self._is_active = False
        player.shadow_color = (0, 0, 0, 0)
        player.pup = None

