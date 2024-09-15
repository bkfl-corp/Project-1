import os
from time import sleep

#https://docs.python.org/3/library/getpass.html#getpass.getpass
from getpass import getpass

from player import Player
from ship import Ship

class Game:
    """
    For managing the overall state of a game of battleship as well as interactions between the players.
    """
    """Initialize Player objects, gets their password for the game, and has them input their ship locations"""
    def __init__(self, num_ships: int) -> None:
        
        print("""================\nWelcome Player 1\n================""")

        self._player_one_pass: str = getpass('Enter your password: ') 
        self._player_one: Player = Game.build_player(num_ships)

        #this clears the screen: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')

        print("""================\nWelcome Player 2\n================""")

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

    #returns a player's set password (VERY NOT SECURE)
    def _get_pass(self, current_player: Player) -> str:
        if current_player == self._player_one:
            return self._player_one_pass
        elif current_player == self._player_two:
            return self._player_two_pass

    #password checking loop
    def check_pass(self, current_player: Player) -> None:
        pass_fail_count: int = 0
        while True:
            check: str = input("Enter your password: ")
            if check == PASS:
                print("PASS")
                pass_fail_count = 0
                break
            else:
                pass_fail_count += 1
            if pass_fail_count >= 5:
                print("Failed to enter password five or more times!\n Please wait five seconds...")
                for x in range (0,5):
                    print(".", end="")
                    sleep(1)
                print("\n")
                pass_fail_count = 0

    def loop(self) -> None:
        """Main gameplay loop. Displays menu and executes choices."""
        turn_count: int = 0 
        current_player: Player = self.player_one #start with player 1
        opponent_player: Player = self.player_two
        made_hit: bool = False
        while True: #loop infinitely! (Until break is called)
            #password check
            self.check_pass(current_player)

            while True:
            print(f"================\nTURN %d\n================" turn_count)
            print("[0] PASS")
            print("[1] CHECK YOUR BOARD")
            print("[2] CHECK YOUR HITS")
            print("[3] MAKE A HIT")
            print("================")
            player_input: str = input("Input: ")
            match player_input:
                case "0":
                    break
                case "1":
                    current_player.display_board_private()
                case "2":
                    opponent_player.display_board_public()
                case "3":
                    if made_hit != True:
                        try:
                            x_coord: int = int(input("Input column number: " ))
                            y_coord: int = int(input("Input row number: " ))
                            opponent_player.take_hit((x_coord, y_coord))
                            #to print "Hit" or "Miss", we need a method from player to check if the hit is true or not
                            
                        except:
                            print("BAD INPUT, TRY AGAIN")
                    else:
                        print("You have already tried a hit this turn")
                case _:
                    print("BAD INPUT, TRY AGAIN")
            
            #check if either p1 or p2's ships are all destroyed
            #(possibly take this block and put it into its own function)
            if self._player_one.num_alive_ships() == 0:
                print("""================\n Player 2 Wins!\n================""")
                break #leave the while loop
            elif self._player_two.num_alive_ships() == 0:
                print("""================\n Player 1 Wins!\n================""")
                break
            else:
                #clear screen
                os.system('cls' if os.name == 'nt' else 'clear')
                #swap current player with opponent player
                temp_player: Player = current_player
                current_player = opponent_player
                opponent_player = temp_player
                made_hit = False
                turn_count += 1
