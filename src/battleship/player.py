from ship import Ship

class Player:
    """
    Manages the state of a players board, as well as displaying said board in various contexts.
    """

    def __init__(self, ships: list[Ship] = []) -> None:
        self._ships: list[Ship] = ships

        #hold the state of the board. the i,j entry of the board represents the if a shot has been fired at coordinate i,j.
        #note that this contains NO information about whether that was a hit or a miss, that information is tracked by each ship.
        self._board_state: bool = [ [ False for _ in range(10) ] for _ in range(10) ]

        self._num_alive_ships = len(self._ships)
    
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

    def display_board_private(self) -> None:
        """Display the state of the board to the player."""
        raise NotImplementedError

    def display_board_public(self) -> None:
        """Display the state of the board to the opponent."""
        raise NotImplementedError

    def add_ship(self, ship: Ship) -> None:
        self._ships.append(ship)
