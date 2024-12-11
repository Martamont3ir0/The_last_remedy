from abc import ABC, abstractmethod


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
    def is_active(self):
        """
        Check if the power-up is currently active.
        """
        pass


class SpeedBoost(PowerUp):
    def __init__(self, duration):
        self._duration = duration
        self._is_active = False

    def apply(self, player):
        player.speed += 10  #Increasing the speed by 10
        self._is_active = True

    def remove(self, player):
        player.speed -= 10  # Revert effect
        self._is_active = False

    def duration(self):
        return self._duration

    def is_active(self):
        return self._is_active

class Invisibility(PowerUp):

    def __init__(self, duration):
        self._duration = duration
        self._is_active = False

    def apply(self, player):
        #Playes becomes invincible and properties on player class change
        player.is_invisible = True


    def remove(self, player):
        #Reverting the change  done on the last function, apply()
        player.is_invincible = False

    def duration(self):
        return self._duration

    def is_active(self):
        return self._is_active

