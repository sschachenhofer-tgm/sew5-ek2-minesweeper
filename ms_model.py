import random


class Field:
    """A class representing a field on the Minesweeper game board.

    This class keeps information about whether the field contains a mine, and whether the field has been tagged.
    """

    # Field states
    COVERED = 0  # The player has not yet uncovered the field
    MINE_TAGGED = 1  # The player has tagged the field as "having a mine"
    MINE_POSSIBLE = 2  # The player has tagged the field as "possibly having a mine"
    UNCOVERED = 3  # The player has uncovered the field

    def __init__(self):
        """Create a new Field instance with no mine and a field state of COVERED.

        The attribute self.mine can be directly updated to add a mine to the Field.
        To update the field state, use the methods switch_tagging() and uncover().
        """
        self.mine = False
        self.state = Field.COVERED

    def switch_tagging(self):
        """Update the field state.

        The field state is switched from COVERED to MINE_TAGGED to MINE_POSSIBLE and back to COVERED.
        Calling switch_tagging() on an UNCOVERED Field will raise an AlreadyUncoveredError.

        :return: The new field state.
        :raises AlreadyUncoveredError: If the Field has been uncovered already
        """
        if self.state == Field.UNCOVERED:
            raise AlreadyUncoveredError
        else:
            self.state = (self.state + 1) % 3
            return self.state

    def uncover(self):
        """Uncover the field

        Only a Field with a field state of COVERED and no mine can be uncovered.

        :raises AlreadyUncoveredError: If the Field has been uncovered already
        :raises FieldTaggedError: If the field is tagged (a tagged field needs to be untagged before it can be
            uncovered)
        :raises MineFound: If the field contains a mine
        """
        if self.state == Field.UNCOVERED:
            # The field has been uncovered already
            raise AlreadyUncoveredError
        elif self.state in [Field.MINE_TAGGED, Field.MINE_POSSIBLE]:
            # The field has been tagged - it needs to be untagged before the player can uncover it
            raise FieldTaggedError
        elif self.mine:
            # There is a mine at the field
            raise MineFound

        else:
            self.state = Field.UNCOVERED


class AlreadyUncoveredError(Exception):
    pass


class FieldTaggedError(Exception):
    pass


class MineFound(Exception):
    pass


class MinesweeperModel:
    """The model class for the Minesweeper game, containing the game logic"""

    def __init__(self, width: int = 9, height: int = 9, n_mines: int = 10):
        """Initialize a new MinesweeperModel for the specified game board

        This creates a game board with the specified dimensions and then randomly hides the specified number of mines.

        :param width: The width (number of columns) of the game board. Default is 9.
        :param height: The height (number of rows) of the game board. Default is 9.
        :param n_mines: The number of mines to hide on the game board. There cannot be more mines than there are fields
            on the game board. Default is 10.

        :raises ValueError: If the number of mines is higher than the number of fields on the game board.
        """
        self.width = width
        self.height = height
        self.n_mines = n_mines
        self.mines = []

        if self.n_mines > self.width * self.height:
            raise ValueError("The number of mines can't be higher than the number of fields on the board")

        # Matrix for storing mines
        # The first value specifies whether there is a mine at the field, the second value specifies the status of the
        # field: covered, tagged (exclamation mark), in question (question mark) or uncovered
        self.__board = [[Field() for i in range(self.height)] for j in range(self.width)]

        # Hide the specified number of mines on the board
        for i in range(n_mines):
            while True:
                # Repeat until a spot on the board is found where the mine can be placed
                x = random.randrange(0, self.width)
                y = random.randrange(0, self.height)

                if not self.__board[x][y].mine:
                    self.__board[x][y].mine = True
                    self.mines.append((x, y))
                    break

    def field_state(self, x: int, y: int) -> int:
        """Get the field state of the specified Field on the game board

        :param x: The x coordinate (column) of the Field (the leftmost column has the x coordinate 0).
        :param y: The y coordinate (row) of the Field (the uppermost row has the y coordinate 0).
        :return: The field state of the specified Field on the game board
        """
        return self.__board[x][y].state

    def switch_tagging(self, x: int, y: int) -> int:
        """Switch the field state of the specified Field on the game board

        :param x: The x coordinate (column) of the Field (the leftmost column has the x coordinate 0).
        :param y: The y coordinate (row) of the Field (the uppermost row has the y coordinate 0).
        :return: The new field state of the specified Field on the game board
        """
        return self.__board[x][y].switch_tagging()

    def uncover(self, x: int, y: int) -> int:
        """Uncover the specified Field on the game board and return the number of mines on adjacent fields

        :param x: The x coordinate (column) of the Field (the leftmost column has the x coordinate 0).
        :param y: The y coordinate (row) of the Field (the uppermost row has the y coordinate 0).
        :return: The number of mines on the adjacent fields (diagonally adjacent fields are counted as well)

        :raises ValueError: If the coordinates outside of the game board bounds
        """
        if x < 0 or x >= self.width:
            raise ValueError(f"Illegal value for x: {x} with width {self.width}")
        if y < 0 or y >= self.height:
            raise ValueError(f"Illegal value for y: {y} with height {self.height}")

        self.__board[x][y].uncover()
        return self.__mines_around(x, y)

    def won(self) -> bool:
        """Check whether all empty Fields have been uncovered

        The game has been won if all empty fields (i.e. all Fields without a mine) have been uncovered.

        :return: True if all Fields without a bomb have been uncovered, False otherwise
        """
        for col in self.__board:
            for field in col:
                if field.state != Field.UNCOVERED and not field.mine:
                    return False

        return True

    def __mines_around(self, x: int, y: int) -> int:
        """Calculate the number of mines on adjacent fields.

        Diagonally adjacent fields (e.g. the field in the top left) are also counted towards adjacent fields.

        :param x: The x coordinate (column) of the Field (the leftmost column has the x coordinate 0).
        :param y: The y coordinate (row) of the Field (the uppermost row has the y coordinate 0).
        :return: The number of mines on the adjacent fields (diagonally adjacent fields are counted as well)

        :raises ValueError: If the coordinates outside of the game board bounds
        """
        if x < 0 or x >= self.width:
            raise ValueError(f"Illegal value for x: {x} with width {self.width}")
        if y < 0 or y >= self.height:
            raise ValueError(f"Illegal value for y: {y} with height {self.height}")

        n = 0

        for temp_x in range(max(0, x - 1), min(self.width, x + 2)):
            for temp_y in range(max(0, y - 1), min(self.height, y + 2)):
                if self.__board[temp_x][temp_y].mine:
                    n += 1

        return n
