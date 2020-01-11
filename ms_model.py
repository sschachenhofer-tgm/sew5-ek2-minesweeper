import enum
import random


class Field:

    COVERED = 0
    MINE_TAGGED = 1
    MINE_POSSIBLE = 2
    UNCOVERED = 3

    def __init__(self):
        self.mine = False
        self.state = Field.COVERED

    def switch_tagging(self):
        if self.state == Field.UNCOVERED:
            raise AlreadyUncoveredError
        else:
            self.state = (self.state + 1) % 3
            return self.state

    def uncover(self):
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
    def __init__(self, width: int = 9, height: int = 9, n_mines: int = 10):
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

    def field_state(self, x, y):
        return self.__board[x][y].state

    def switch_tagging(self, x, y):
        return self.__board[x][y].switch_tagging()

    def uncover(self, x: int, y: int) -> int:
        if x < 0 or x >= self.width:
            raise ValueError(f"Illegal value for x: {x} with width {self.width}")
        if y < 0 or y >= self.height:
            raise ValueError(f"Illegal value for y: {y} with height {self.height}")

        self.__board[x][y].uncover()
        return self.__mines_around(x, y)

    def __mines_around(self, x, y) -> int:
        if x < 0 or x >= self.width:
            raise ValueError("Illegal value for x")
        if y < 0 or y >= self.height:
            raise ValueError("Illegal value for y")

        n = 0

        for temp_x in range(max(0, x - 1), min(self.width, x + 2)):
            for temp_y in range(max(0, y - 1), min(self.height, y + 2)):
                if self.__board[temp_x][temp_y].mine:
                    n += 1

        return n
