import os

#https://docs.python.org/3/library/getpass.html#getpass.getpass
from getpass import getpass

from player import Player
from ship import Ship

class Game:
    """
    For managing the overall state of a game of battleship as well as interactions between the players.
    """
    
    def __init__(self, num_ships: int) -> None:
        
        print("""================
                 Welcome Player 1
                 ================""")

        self._player_one_pass: str = getpass('Enter your password: ') 
        self._player_one: Player = Game.build_player(num_ships)

        #this clears the screen: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')

        print("""================
                 Welcome Player 2
                 ================""")

        self._player_two_pass: str = getpass('Enter your password: ')
        self._player_two: Player = Game.build_player(num_ships)

        #this clears the screen: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def build_player(num_ships: int) -> Player:
        """Talk to the user and initialize a player object."""
        
        player: Player = Player()

        ship_length: int = 0
        
        for _ in range(num_ships):
            
            ship_length += 1

            while True:

                player.display_board_private()

                try:
                    start_coord: tuple[int, int] = tuple(map(int, input(f'Enter starting x,y coordinate for a ship that is {ship_length} long: ').split(',')))
                    end_coord: tuple[int, int] = tuple(map(int, input(f'Enter ending x,y coordinate: ').split(',')))
                    ship: Ship = Ship(ship_length, start_coord, end_coord)
                    player.add_ship(ship)
                    break

                except ValueError:
                    continue

        return player

    def loop(self) -> None:
        """Main gameplay loop. Displays menu and executes choices."""

        raise NotImplementedError


