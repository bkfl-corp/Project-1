class Ship:
    """
    Represents a particular ship on the board, as well as the health of said ship.
    """

    def __init__(self, ship_length: int, start_coord: tuple[int, int], end_coord: tuple[int, int]) -> None:

        if not (1 < ship_length < 11):
            raise ValueError('Invalid ship length! Must be between 1 and 10.')

        self._ship_length: int = ship_length

        if not (0,0) <= start_coord <= (9,9):
            raise ValueError('Invalid start coordinate! Must be between (0,0) and (9,9).')

        if not (0,0) <= end_coord <= (9,9):
            raise ValueError('Invalid end coordinate! Must be between (0,0) and (9,9).')
        
        if start_coord > end_coord:
            raise ValueError('Start coordinate is bigger than end coordinate. Maybe swapped coordinates?')

        if end_coord[0] - start_coord[0] == self._ship_length and end_coord[1] - start_coord[1] == self._ship_length:
            raise ValueError('Tried to place ship in coordinates that don\'t match length.')
        
        #implies horizontal placement.
        if start_coord[0] == end_coord[0]:
            self._hull: tuple[int, int, bool] = [(start_coord[0], y, False) for y in range(start_coord[1], end_coord[1]+1)]

        #implies vertical placement.
        elif start_coord[1] == start_coord[1]:
            self._hull: tuple[int, int, bool] = [(x, start_coord[1], False) for x in range(start_coord[0], end_coord[0]+1)]

        else:
            raise('Invalid ship placement! Make sure that it is horizontal or vertical.')

        self.sunk: bool = False
    
    @property
    def ship_length(self) -> int:
        """Length of ship as an immutable attribute."""
        return self._ship_length

    @property
    def hull(self) -> list[tuple[int, int, bool]]:
        return self._hull

    def take_hit(self, coordinate: tuple[int, int]) -> None:
        raise NotImplementedError

        return None