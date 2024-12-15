from abc import ABC, abstractmethod
import time

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

    @abstractmethod
    def duration(self):
        """
        Return the duration of the power-up effect.
        """
        pass

    @abstractmethod
    def is_active(self,player):
        """
        Check if the power-up is currently active.
        """
        pass


class SpeedBoost(PowerUp):
    def __init__(self, duration):
        self._duration = duration
        self._is_active = False
        self._start_time = None

    def apply(self, player):
        player.speed += 10  # Increasing the speed by 10
        self._is_active = True
        self._start_time = time.time()  # Record the time when the power-up is applied

    def remove(self, player):
        player.speed -= 10  # Revert effect
        self._is_active = False

    def duration(self):
        return self._duration

    def is_active(self,player):
        if self._is_active and (time.time() - self._start_time >= self._duration):
            self.remove(player)  # Automatically remove if duration has passed
        return self._is_active


class Invincibility(PowerUp):
    def __init__(self, duration):
        self._duration = duration
        self._is_active = False
        self._start_time = None

    def apply(self, player):
        player.is_invincible = True
        self._is_active = True
        self._start_time = time.time()  # Record the time when the power-up is applied

    def remove(self, player):
        player.is_invincible = False
        self._is_active = False

    def duration(self):
        return self._duration

    def is_active(self,player):
        if self._is_active and (time.time() - self._start_time >= self._duration):
            self.remove(player)  # Automatically remove if duration has passed
        return self._is_active


class HealthRegeneration(PowerUp):
    def __init__(self, duration, regeneration_amount):
        self._regeneration_amount = regeneration_amount
        self._duration = duration
        self._is_active = False

    def apply(self, player):
        self._is_active = True
        player.health += self._regeneration_amount  # Apply the regeneration immediately
        player.health = min(player.health, 100)  # Cap health at max (e.g., 100)

    def remove(self, player):
        self._is_active = False

    def duration(self):
        return self._duration

    def is_active(self,player):
        return self._is_active

