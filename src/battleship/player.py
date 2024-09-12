from ship import Ship

class Player:
    """
    Manages the state of a players board, as well as displaying said board in various contexts.
    """

    def __init__(self, ships: list[Ship] = []) -> None:
        self._ships: list[Ship] = ships

        #hold the state of the board. the i,j entry of the board represents the if a shot has been fired at coordinate i,j.
        #note that this contains NO information about whether that was a hit or a miss, that information is tracked by each ship.
        self._board_state: list[list[bool]] = [ [ False for _ in range(10) ] for _ in range(10) ]

        self._num_alive_ships: int = len(self._ships)
    
    @property
    def num_ships(self) -> int:
        return len(self._ships)

    @property
    def num_alive_ships(self) -> int:
        return self._num_alive_ships

    @property
    def num_sunk_ships(self) -> int:
        return self.num_ships - self.num_alive_ships

    def take_hit(self, coordinate: tuple[int, int]) -> None:
        """Update the state of the board and ships."""
        raise NotImplementedError

    def _get_cell_state(self, i: int, j: int, private: bool) -> str:
        """Serve as a helper method to get the state of each cell for private and public boards."""
        # Check if the cell is part of any ship
        for ship in self._ships:
            for x, y, hit in ship.hull:
                if (i, j) == (x, y):
                    if ship.sunk:
                        return '@' # Sunken ship
                    elif hit:
                        return 'X' # Hit ship
                    elif private:
                        return 'S' # Ship but not hit (only visible in private view)

        # No ship in this cell
        if self._board_state[i][j]:
            return 'O' # Shot at, but missed
        return '~' # Unshot cell

    def display_board_private(self) -> None:
        """Display the state of the board to the player."""
        print("  " + " ".join(str(i) for i in range(10))) # Print top border numbers
        print(" +" + "-" * 21 + "+") # Top border

        for i in range(10):
            row: list[str] = [self._get_cell_state(i, j, private=True) for j in range(10)]
            print(f"{i}| {' '.join(row)} |") # Board with side borders & side boarder numbers
        
        print(" +" + "-" * 21 + "+") # Bottom border

    def display_board_public(self) -> None:
        """Display the state of the board to the opponent."""
        print("  " + " ".join(str(i) for i in range(10))) # Print top border numbers
        print(" +" + "-" * 21 + "+") # Top border

        for i in range(10):
            row: list[str] = [self._get_cell_state(i, j, private=False) for j in range(10)]
            print(f"{i}| {' '.join(row)} |") # Board with side borders & side boarder numbers

        print(" +" + "-" * 21 + "+") # Bottom border

    def add_ship(self, ship: Ship) -> None:
        self._ships.append(ship)
