import random


class MineFound(Exception):
    pass


class AlreadyUncoveredError(Exception):
    pass


class MinesweeperModel:
    def __init__(self, width: int = 9, height: int = 9, mines: int = 10):
        self.width = width
        self.height = height
        self.mines = mines

        if self.mines > self.width * self.height:
            raise ValueError("The number of mines can't be higher than the number of fields on the board")

        # Matrix for storing mines
        # The first value specifies whether there is a mine at the field, the second value specifies whether the field
        # has been uncovered.
        self.board = [[(False, False) for i in range(self.height)] for j in range(self.width)]

        # Hide the specified number of mines on the board
        for i in range(mines):
            while True:
                # Repeat until a spot on the board is found where the mine can be placed
                x = random.randrange(0, self.width)
                y = random.randrange(0, self.height)

                if not self.board[x][y][0]:
                    self.board[x][y] = (True, False)
                    break

    def __mines_around(self, x, y) -> int:
        if x < 0 or x >= self.width:
            raise ValueError("Illegal value for x")
        if y < 0 or y >= self.height:
            raise ValueError("Illegal value for y")

        n = 0

        for temp_x in range(max(0, x - 1), min(self.width, x + 2)):
            for temp_y in range(max(0, y - 1), min(self.height, y + 2)):
                if self.board[temp_x][temp_y]:
                    n += 1

        return n

    def uncover(self, x: int, y: int) -> int:
        if x < 0 or x >= self.width:
            raise ValueError("Illegal value for x")
        if y < 0 or y >= self.height:
            raise ValueError("Illegal value for y")

        if self.board[x][y][1]:
            # The field has been uncovered already
            raise AlreadyUncoveredError
        elif self.board[x][y][0]:
            # There is a mine at the field
            raise MineFound
        else:
            # Calculate the number of mines surrounding the field
            return self.__mines_around(x, y)
