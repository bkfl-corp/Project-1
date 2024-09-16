"""
Name of program: game.py
Description: Class to control game and game state.
Inputs: None
Outputs: None
Other sources for code: N/A
Authors: James Hurd, Joshua Lee, Will Whitehead, Trent Gould, Ky Le
Creation date: 09/11/25
"""

#used for clearing the screen, as we need to know what is we are on to send the proper control character.
import os

#used for getting passwords: https://docs.python.org/3/library/getpass.html#getpass.getpass
from getpass import getpass

#import player class.
from player import Player

#import ship class.
from ship import Ship

#import exception that denotes invalid ship length.
from exceptions import InvalidShipLengthError, InvalidCoordinatesError, AlreadyFiredError

class Game:
    """
    For managing the overall state of a game of battleship as well as interactions between the players.
    """

    def __init__(self, num_ships: int) -> None:
        """Initialize Player objects, gets their password for the game, and has them input their ship locations"""
        
        #print welcome message.
        print('================\nWelcome Player 1\n================')
        
        #get player name.
        player_one_name: str = input('What\'s your name? ')

        #get player password.
        self._player_one_pass: str = getpass('Enter your password: ') 

        #create player 1 object.
        self._player_one: Player = Game._build_player(player_one_name, num_ships)

        #this clears the screen: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')
        
        #print welcome message
        print('================\nWelcome Player 2\n================')
        
        #get player name.
        player_two_name: str = input('What\'s your name? ')

        #get player password.
        self._player_two_pass: str = getpass('Enter your password: ')

        #build player 2 object.
        self._player_two: Player = Game._build_player(player_two_name, num_ships)

        #this clears the screen: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def _build_player(name: str, num_ships: int) -> Player:
        """Talk to the user and initialize a player object."""
        
        player: Player = Player(name)

        ship_length: int = 0
        
        for _ in range(num_ships):
            
            ship_length += 1

            while True:

                player.display_board_private()

                try:
                    # Allow either "A1" or "A,1" format for input
                    start_coord_input = input(f'Enter starting coordinate for a ship that is {ship_length} long (e.g., A1 or A,1): ').replace(' ', '').upper()
                    start_coord = Game._parse_coordinate(start_coord_input)

                    end_coord_input = input(f'Enter ending coordinate for the ship (e.g., A1 or A,1): ').replace(' ', '').upper()
                    end_coord = Game._parse_coordinate(end_coord_input)

                    ship: Ship = Ship(ship_length, start_coord, end_coord)
                    
                    try:
                        player.add_ship(ship)
            
                    except ValueError:
                        print('This placement intersects another ship, please try again.')
                        continue

                    break

                except (InvalidShipLengthError, InvalidCoordinatesError) as e:
                    print(f'[ERROR] {e} Please try again.')
                    continue

        return player

    
    @staticmethod
    def _parse_coordinate(input_str: str) -> tuple[int, int]:
        """Converts a string in 'A1' or 'A,1' format to a tuple of ints (row, col)"""
        input_str = input_str.replace(' ', '').upper()  # Remove spaces and normalize to uppercase

        # Allow either "A1" or "A,1" format for input
        if ',' in input_str:  # Format is A,1
            col_str, row_str = input_str.split(',')
        else:  # Format is A1
            col_str, row_str = input_str[0], input_str[1:]

        # Validate the row and column
        if not row_str.isdigit() or len(row_str) > 2:
            raise InvalidCoordinatesError(f"Invalid row number '{row_str}'. Please use a number between 1 and 10.")

        row = int(row_str) - 1  # Convert row to 0-indexed
        col_num: int = "ABCDEFGHIJ".find(col_str)
        if col_num == -1 or not (0 <= row <= 9):
            raise InvalidCoordinatesError("Coordinate not on board. Please use a valid format (e.g., A1 or A,1).")

        return (row, col_num)


    #password checking loop
    def _check_pass(self, player: Player) -> None:
        player_pass: str = self._player_one_pass if player is self._player_one else self._player_two_pass

        while True:
            check: str = getpass(f'[{player.name}]: Enter your password: ')
            if check == player_pass:
                break

            print('Incorrect! Please try again.')

    def loop(self) -> None:
        """Main gameplay loop. Displays menu and executes choices."""
        turn_count: int = 0 
        current_player: Player = self._player_one #start with player 1
        opponent_player: Player = self._player_two
        while True: #loop infinitely! (Until break is called)
            #password check
            self._check_pass(current_player)
        
            while True:
                print(f'================\nTURN {turn_count}\n================')
                print('[0] CHECK YOUR BOARD\n[1] CHECK OPPONENTS BOARD\n[2] FIRE\n================')
                try:
                    player_input: int = int(input('What would you like to do?: '))

                    if not 0 <= player_input <= 3:
                        raise ValueError

                except ValueError:
                    print('Invalid input, please choose off of the menu.')
                    continue

                match player_input:
                    case 0:
                        current_player.display_board_private()
                    case 1:
                        opponent_player.display_board_public()
                    case 2:
                        try:
                            opponent_player.display_board_public()
                            coord_input = input(f'Enter a coordinate to fire (e.g., A1 or A,1): ').replace(' ', '').upper()
                            coord: tuple[int, int] = Game._parse_coordinate(coord_input)

                            print('Hit!' if opponent_player.take_hit(coord) else 'Miss!')

                            opponent_player.display_board_public()
                            input('Press ENTER to continue')
                            break
                                
                        except (AlreadyFiredError, InvalidCoordinatesError) as e:
                            print(e)



                            

            #check if either p1 or p2's ships are all destroyed
            #(possibly take this block and put it into its own function)
            if opponent_player.num_alive_ships == 0:
                print(f'================\n {self._player_two.name} Wins!\n================')
                break #leave the while loop

            #clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            #swap current player with opponent player
            temp_player: Player = current_player
            current_player = opponent_player
            opponent_player = temp_player
            turn_count += 1
