from abc import ABC, abstractmethod
import time
import pygame



class PowerUp(ABC):
    @abstractmethod
    def apply(self, player):
        """
        Apply the power-up effect to the player.
        """
        pass

    @abstractmethod
    def remove(self, player):
        """
        Remove the power-up effect from the player.
        """
        pass






class SpeedBoost(PowerUp):

    def __init__(self, duration):
        super().__init__()
        self._duration = duration
        self._is_active = False

    def apply(self, player):

        player.speed += 8  # Increase the speed by 8
        player.pup = "SpeedBoost"  # Set the player's current power-up
        player.feelings = "like a SuperHero"
        print(f"SpeedBoost applied.")

    def remove(self, player):

        player.speed -= 8  # Revert effect
        player.pup = None  # Clear the power-up from the player
        self._is_active = False
        print("SpeedBoost removed.")


class Invincibility(PowerUp):
    def __init__(self, duration):
        super().__init__()
        self._duration = duration
        self._is_active = False


    def apply(self, player):
        player.is_invincible = True
        self._is_active = True
        player.pup = "Invincibility"
        player.feelings = "like Captain America"
        print("Shield applied.")

    def remove(self, player):
        player.is_invincible = False
        player.pup = None
        self._is_active = False

        print("Shield removed.")

class HealthRegeneration(PowerUp):
    def __init__(self, regeneration_amount):
        super().__init__()
        self._regeneration_amount = regeneration_amount
        self._is_active = False

    def apply(self, player):
        self._is_active = True
        player.health += self._regeneration_amount  # Apply the regeneration immediately
        player.health = min(player.health, 100)  # Cap health at max (e.g., 100)
        player.pup = "Health Regeneration"
        player.feelings = "refreshed"
        print("Health applied.")
    def remove(self, player):
        self._is_active = False
        player.pup = None

class Sadness(PowerUp):
    def __init__(self):
        super().__init__()
        self._is_active = False

    def apply(self, player):
        self._is_active = True
        player.feelings = "EXTRA Sad"
        player.pup = "Sadness"
        print("Sadness applied.")
    def remove(self, player):
        self._is_active = False
        player.pup = None

