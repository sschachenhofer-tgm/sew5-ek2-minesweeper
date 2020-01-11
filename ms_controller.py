import time

from PyQt5.QtCore import QSignalMapper, Qt
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QMainWindow, QPushButton, QSizePolicy

from ms_window import Ui_MainWindow
from ms_model import *
from ms_custom_game_dialog import Ui_Dialog


class CustomGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = Ui_Dialog()
        self.view.setupUi(self)

        self.setModal(True)
        self.view.buttonBox.accepted.connect(self.accept)
        self.view.buttonBox.rejected.connect(self.reject)


class MinesweeperController(QMainWindow):
    """The minesweeper controller class, responsible for handling user input"""

    # Reusable stylesheet blocks
    RED_BG = "background-color: red; color: black;"
    YELLOW_BG = "background-color: yellow; color: black;"
    BLUE_BG = "background-color: blue; color: white;"
    GREEN_BG = "background-color: green; color: black;"
    FONT = "font-weight: 1000; font-size: 17px;"
    NO_BORDER = "border: none;"

    # Stylesheet constants for quick styling of fields
    MINE_MISSED_STYLE = f"* {{ {RED_BG} {FONT} {NO_BORDER} }}"  # For mines the player hasn't found until the game ended
    MINE_FOUND_STYLE = f"* {{ {GREEN_BG} {FONT} {NO_BORDER} }}"  # For mines the player had tagged before the game ended
    MINE_TAGGED_STYLE = f"* {{ {YELLOW_BG} {FONT} {NO_BORDER} }}"  # For fields the player tagged as "mine"
    MINE_POSSIBLE_STYLE = f"* {{ {BLUE_BG} {FONT} {NO_BORDER} }}"  # For fields the player tagged as "possibly a mine"

    # Font styles for the labels specifying the number of adjacent mines - these are the original Minesweeper colors
    UNCOVERED_STYLE = [
        "",  # Fields with 0 bordering mines don't have any text
        f"* {{ color: #0200fd; {FONT} {NO_BORDER} }}",  # 1 mine
        f"* {{ color: #017e00; {FONT} {NO_BORDER} }}",  # 2 mines
        f"* {{ color: red; {FONT} {NO_BORDER} }}",      # 3 mines
        f"* {{ color: #010180; {FONT} {NO_BORDER} }}",  # 4 mines
        f"* {{ color: #7f0300; {FONT} {NO_BORDER} }}",  # 5 mines
        f"* {{ color: #008180; {FONT} {NO_BORDER} }}",  # 6 mines
        f"* {{ color: black; {FONT} {NO_BORDER} }}",    # 7 mines
        f"* {{ color: #808080; {FONT} {NO_BORDER} }}",  # 8 mines
    ]

    def __init__(self, columns: int = 9, rows: int = 9, mines: int = 10):
        """Initialize a game of Minesweeper

        This will create the game board and hide the specified number of mines on the board.

        :param columns: The number of columns on the game board (the width). Default is 9.
        :param rows: The number of rows on the game board (the height). Default is 9.
        :param mines: The number of mines to hide on the game board. There cannot be more mines on the game board than
            there are fields. Default is 10.
        """
        super().__init__(parent=None)

        # These attributes will be initialized in __new_game()
        self.columns = 0
        self.rows = 0
        self.mines = 0
        self.game_running = False

        # Initialize the GUI
        self.view = Ui_MainWindow()
        self.view.setupUi(self)

        # Connect the signals of the "New game" buttons
        self.view.new_game_easy.triggered.connect(self.easy_game)
        self.view.new_game_medium.triggered.connect(self.medium_game)
        self.view.new_game_difficult.triggered.connect(self.difficult_game)
        self.view.new_game_custom.triggered.connect(self.custom_game_dialog)

        # The model will be initialized in __new_game()
        self.model = None

        # A dialog window for starting a custom game
        self.dialog = CustomGameDialog()
        self.dialog.accepted.connect(self.__custom_game)

        # Initialize a QSignalMapper to enable mapping all button clicks to a single method
        self.mapper = QSignalMapper(self.view.centralwidget)
        self.mapper.mapped.connect(self.button_clicked)

        # Initialize another QSignalMapper to enable mapping of right-clicks
        self.rc_mapper = QSignalMapper(self.view.centralwidget)
        self.rc_mapper.mapped.connect(self.button_right_clicked)

        # Create a QGridLayout for the buttons
        self.grid = QGridLayout()
        self.view.main_layout.addLayout(self.grid)
        self.grid.setSpacing(5)

        # This is the only efficient way to keep a reference to all buttons on the board, since buttons are
        # "re-parented" to the main window after being added to a layout
        self.buttons = []

        self.grid.setSizeConstraint(QGridLayout.SetFixedSize)

        self.__new_game(columns=columns, rows=rows, mines=mines)

    def button_clicked(self, position: int) -> None:
        """Handle a click event on a button on the game board

        If the field underneath the button contains a mine, the game ends and a message is displayed.
        If the field underneath the button is currently tagged (displayed as exclamation mark (!) or question mark (?)
        on the game board, the field will not be uncovered and instead a message is displayed.
        Otherwise, the field is uncovered. The button is replaced by a label displaying the number of mines on the
        adjacent fields. If no adjacent field contains a mine, the untagged, uncovered adjacent fields will be
        uncovered as well.

        :param position: The position of the button (width * y + x)
        """
        x = position % self.columns
        y = int(position / self.columns)

        if self.game_running:
            self.__uncover_field(x, y)
        else:
            self.view.statusbar.showMessage("You need to restart the game!", 5000)

    def button_right_clicked(self, position: int) -> None:
        """Handle a right-click event on a button on the game board.

        Right-clicks tag the corresponding field. A field can be tagged as "having a mine" (displayed as an exclamation
        mark "!") or as "possibly having a mine" (displayed as a question mark "?"). Right-clicking a field switches
        between the states untagged, "having a mine" and "possibly having a mine". A tagged field cannot be uncovered.

        :param position: The position of the button (width * y + x)
        """
        x = position % self.columns
        y = int(position / self.columns)

        if self.game_running:
            self.__tag_field(x, y)
        else:
            self.view.statusbar.showMessage("You need to restart the game!", 5000)

    def easy_game(self) -> None:
        """Start a new game on a 9x9 board with 10 mines"""
        self.__new_game()

    def medium_game(self) -> None:
        """Start a new game on a 16x16 board with 40 mines"""
        self.__new_game(columns=16, rows=16, mines=40)

    def difficult_game(self) -> None:
        """Start a new game on a 30x16 board with 99 mines"""
        self.__new_game(columns=30, rows=16, mines=99)

    def custom_game_dialog(self) -> None:
        """Open a dialog window for the player to choose custom board dimensions and the number of mines"""
        self.dialog.exec()

    def __custom_game(self) -> None:
        """Read the values for the custom game from the QDialog and start the game"""
        cols = self.dialog.view.columns.value()
        rows = self.dialog.view.rows.value()
        mines = self.dialog.view.mines.value()
        self.__new_game(columns=cols, rows=rows, mines=mines)

    def __new_game(self, columns: int = 9, rows: int = 9, mines: int = 10) -> None:
        """Start a new game of Minesweeper

        This will create the game board and hide the specified number of mines on the board.

        :param columns: The number of columns on the game board (the width). Default is 9.
        :param rows: The number of rows on the game board (the height). Default is 9.
        :param mines: The number of mines to hide on the game board. There cannot be more mines on the game board than
            there are fields. Default is 10.
        """
        self.columns = columns
        self.rows = rows
        self.mines = mines
        self.game_running = True

        # Initialize a new model
        self.model = MinesweeperModel(width=self.columns, height=self.rows, n_mines=mines)

        # Clear the QGridLayout
        while True:
            item = self.grid.takeAt(0)
            if item is None:
                break
            else:
                self.grid.removeItem(item)
                item.widget().deleteLater()

        # Clear the list of buttons
        self.buttons.clear()

        # Add the buttons to the GUI
        for n in range(self.columns * self.rows):
            # Create the QPushButton
            button = QPushButton()
            button.setFixedSize(40, 40)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            # Connect the button signals
            self.mapper.setMapping(button, n)
            button.clicked.connect(self.mapper.map)  # For left-clicks
            self.rc_mapper.setMapping(button, n)
            button.customContextMenuRequested.connect(self.rc_mapper.map)  # For right-clicks
            button.setContextMenuPolicy(Qt.CustomContextMenu)  # For enabling the customContextMenuRequested signal

            # Add the button to the QGridLayout
            self.grid.addWidget(button, int(n / self.columns), n % self.columns, alignment=Qt.AlignCenter)
            self.buttons.append(button)

        # Resize the grid rows
        for i in range(self.grid.rowCount()):
            self.grid.setRowMinimumHeight(i, 40)

        # Resize the grid columns
        for i in range(self.grid.columnCount()):
            self.grid.setColumnMinimumWidth(i, 40)

        # For some reason, it really is that complicated to resize the window appropiately...
        window_width = self.columns * 45 + 18
        window_height = self.rows * 45 + 18 \
                        + self.view.menubar.sizeHint().height() \
                        + self.view.statusbar.sizeHint().height() \
                        + 18

        # self.setFixedSize(window_width, window_height)
        self.resize(window_width, window_height)

    def __uncover_field(self, x: int, y: int) -> None:
        """Uncover a field on the game board

        This method uncovers a field on the game board. If the field underneath the button contains a mine, the game
        ends and a message is displayed. If the field underneath the button is currently tagged (displayed as
        exclamation mark (!) or question mark (?) on the game board, the field will not be uncovered.

        Otherwise, the field is uncovered. The button is replaced by a label displaying the number of mines on the
        adjacent fields. If no adjacent field contains a mine, the untagged, uncovered adjacent fields will be
        uncovered as well.

        :param x: The x coordinate (column) of the field to uncover (the leftmost column has the x coordinate 0).
        :param y: The y coordinate (row) of the field to uncover (the uppermost row has the y coordinate 0).
        """
        try:
            n = self.model.uncover(x, y)

            # The grid layout is accessed by row and column (y, x) instead of x, y
            button = self.grid.itemAtPosition(y, x).widget()

            # Replace the button with a label displaying the number of adjacent mines
            label = QLabel(str(n) if n > 0 else "")
            label.setStyleSheet(MinesweeperController.UNCOVERED_STYLE[n])
            self.grid.replaceWidget(button, label, options=Qt.FindChildrenRecursively)

            # Delete the button
            button.deleteLater()
            self.buttons.remove(button)

            # If the field has 0 adjacent bombs, uncover the four directly surrounding fields as well
            if n == 0:
                if x - 1 >= 0 and self.model.field_state(x - 1, y) == Field.COVERED:
                    self.__uncover_field(x - 1, y)  # Left field
                if x - 1 >= 0 and y - 1 >= 0 and self.model.field_state(x - 1, y - 1) == Field.COVERED:
                    self.__uncover_field(x - 1, y - 1)  # Top left field
                if y - 1 >= 0 and self.model.field_state(x, y - 1) == Field.COVERED:
                    self.__uncover_field(x, y - 1)  # Top field
                if x + 1 < self.columns and y - 1 >= 0 and self.model.field_state(x + 1, y - 1) == Field.COVERED:
                    self.__uncover_field(x + 1, y - 1)  # Top right field
                if x + 1 < self.columns and self.model.field_state(x + 1, y) == Field.COVERED:
                    self.__uncover_field(x + 1, y)  # Right field
                if x + 1 < self.columns and y + 1 < self.rows and self.model.field_state(x + 1, y + 1) == Field.COVERED:
                    self.__uncover_field(x + 1, y + 1)  # Bottom right field
                if y + 1 < self.rows and self.model.field_state(x, y + 1) == Field.COVERED:
                    self.__uncover_field(x, y + 1)  # Bottom field
                if x - 1 >= 0 and y + 1 < self.rows and self.model.field_state(x - 1, y + 1) == Field.COVERED:
                    self.__uncover_field(x - 1, y + 1)  # Bottom left field

        except AlreadyUncoveredError:
            pass
        except FieldTaggedError:
            self.view.statusbar.showMessage("You need to untag the field before you can open it", 5000)
        except MineFound:
            self.__end_game(won=False)

        if self.model.won():
            self.__end_game(won=True)

    def __tag_field(self, x: int, y: int) -> None:
        """Tag a field on the game board.

        A field can be tagged as "having a mine" (displayed as an exclamation
        mark "!") or as "possibly having a mine" (displayed as a question mark "?"). Right-clicking a field switches
        between the states untagged, "having a mine" and "possibly having a mine". A tagged field cannot be uncovered.

        :param x: The x coordinate (column) of the field to uncover (the leftmost column has the x coordinate 0).
        :param y: The y coordinate (row) of the field to uncover (the uppermost row has the y coordinate 0).
        """
        try:
            # The grid layout is accessed by row and column (y, x) instead of x, y
            button = self.grid.itemAtPosition(y, x).widget()

            new_state = self.model.switch_tagging(x, y)
            if new_state == Field.COVERED:
                button.setStyleSheet("")
                button.setText("")
            elif new_state == Field.MINE_TAGGED:
                button.setStyleSheet(MinesweeperController.MINE_TAGGED_STYLE)
                button.setText("!")
            elif new_state == Field.MINE_POSSIBLE:
                button.setStyleSheet(MinesweeperController.MINE_POSSIBLE_STYLE)
                button.setText("?")

        except AlreadyUncoveredError:
            pass

    def __end_game(self, won: bool = False) -> None:
        """End the game

        This method ends the game by disabling all buttons, displaying the positions of the mines on the game board
        and displaying a message for the user.

        :param won: True if the game has been won (i.e. all fields without a mine have been uncovered), False if the
            game has been lost (i.e. the player tried to uncover a field with a mine)
        """
        # End the game
        self.game_running = False

        # Disable all buttons
        for button in self.buttons:
            button.setEnabled(False)

        # Show the mine positions:
        for x, y in self.model.mines:
            # The grid layout is accessed by row and column (y, x) instead of x, y
            widget = self.grid.itemAtPosition(y, x).widget()
            widget.setText("\u2715")

            if self.model.field_state(x, y) == Field.COVERED:
                widget.setStyleSheet(MinesweeperController.MINE_MISSED_STYLE)
            else:
                widget.setStyleSheet(MinesweeperController.MINE_FOUND_STYLE)

        # Display a message - TODO: Open a dialog instead
        self.view.statusbar.showMessage("You won :)" if won else "You lost :)", 5000)
