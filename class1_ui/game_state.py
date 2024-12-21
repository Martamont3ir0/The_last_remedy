import json
from player import Player
from shed_characters import *

class GameState:
    def __init__(self, player, monster, cactus_group, coins):
        """
        Initialize the GameState with the current player, monster, cactus_group, and coins.

        :param player: The player object containing player attributes.
        :param monster: Monster object in the game.
        :param cactus_group: A list of cactus objects in the game.
        :param coins: A list of coin objects in the game.
        """
        self.player = player  # Store the player object
        self.monster = monster  # Store the monster
        self.cactus_group = cactus_group  # Store the list of cacti
        self.coins = coins  # Store the list of coins

    def save(self, filename):
        """
        Save the current game state to a JSON file.

        :param filename: The name of the file to save the game state to.
        """
        # Create a dictionary representation of the game state
        state = {
            'player': {
                'health': self.player.health,  # Save player's health
                'money': self.player.money,  # Save player's money
                'position': self.player.position,  # Save player's position
                'level':self.player.level #Save most recent level
            },
            'monster': [monster.to_dict() for monster in self.monster],  # Save each monster's state
            'cactus_group': [cactus.to_dict() for cactus in self.cactus_group],  # Save each cactus' state
            'coins': [coin.to_dict() for coin in self.coins],  # Save each coin's state
        }

        # Write the state dictionary to a JSON file
        with open(filename, 'w') as f:
            json.dump(state, f, indent=4)  # Save with pretty printing

    @classmethod
    def load(cls, filename):
        """
        Load the game state from a JSON file and return a GameState object.

        :param filename: The name of the file to load the game state from.
        :return: An instance of GameState populated with the loaded data.
        """
        with open(filename, 'r') as f:
            state = json.load(f)  # Load the state from the JSON file

        # Create a new player object with loaded attributes
        player = Player()
        player.health = state['player']['health']
        player.money= state['player']['money']
        player.position = state['player']['position']  # Set player's position
        player.level = state['player']['level']  # Set game level
        # Create lists of monster, cactus_group, and coins from the loaded data
        monster = [Monster.from_dict(data) for data in state['monster']]
        cactus_group = [Cactus.from_dict(data) for data in state['cactus_group']]
        coins = [Coin.from_dict(data) for data in state['coins']]

        # Return a new GameState object with the loaded data
        return cls(player, monster, cactus_group, coins)