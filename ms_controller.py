from PyQt5.QtCore import QSignalMapper, Qt
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout

from ms_window import Ui_MainWindow
from ms_model import *


class MinesweeperController(QMainWindow):

    RED_BG = "background-color: red; color: black;"
    BLUE_BG = "background-color: blue; color: white;"
    GREEN_BG = "background-color: green; color: black;"
    FONT = "font-weight: 1000; font-size: 2em;"
    NO_BORDER = "border: none;"

    MINE_MISSED_STYLE = f"* {{ {RED_BG} {FONT} {NO_BORDER} }}"
    MINE_FOUND_STYLE = f"* {{ {GREEN_BG} {FONT} {NO_BORDER} }}"

    MINE_TAGGED_STYLE = f"* {{ {RED_BG} {FONT} {NO_BORDER} }}"
    MINE_POSSIBLE_STYLE = f"* {{ {BLUE_BG} {FONT} {NO_BORDER} }}"
    UNCOVERED_STYLE = f"* {{ {FONT} }}"

    def __init__(self, columns: int = 9, rows: int = 9, mines: int = 10):
        super().__init__(parent=None)

        self.columns = columns
        self.rows = rows
        self.mines = mines
        self.game_running = True

        print(f"Board dimensions: {self.columns}x{self.rows}, {self.mines} mines")

        # Initialize the GUI
        self.view = Ui_MainWindow()
        self.view.setupUi(self)

        # Initialize the model
        self.model = MinesweeperModel(self.columns, self.rows, mines)

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

        # This is the only way to keep a reference to all buttons on the board, since buttons are "re-parented" to the
        # main window after being added to a layout
        self.buttons = []

        # Add the buttons to the GUI
        for n in range(self.columns * self.rows):
            button = QPushButton()
            button.setFixedSize(40, 40)

            # Connect the button signals
            self.mapper.setMapping(button, n)
            self.rc_mapper.setMapping(button, n)
            button.clicked.connect(self.mapper.map)
            button.customContextMenuRequested.connect(self.rc_mapper.map)
            button.setContextMenuPolicy(Qt.CustomContextMenu)

            self.grid.addWidget(button, int(n / self.columns), n % self.columns, alignment=Qt.AlignCenter)
            self.buttons.append(button)

        # Resize the rows
        for i in range(self.grid.rowCount()):
            self.grid.setRowMinimumHeight(i, 40)

        # Resize the columns
        for i in range(self.grid.columnCount()):
            self.grid.setColumnMinimumWidth(i, 40)

        self.grid.setSizeConstraint(QGridLayout.SetFixedSize)

        # For some reason, it really is that complicated to resize the window appropiately...
        window_width = self.view.main_layout.sizeHint().width() + 18
        window_height = self.view.main_layout.sizeHint().height() \
                        + self.view.menubar.sizeHint().height() \
                        + self.view.statusbar.sizeHint().height() \
                        + 18

        self.setFixedSize(window_width, window_height)

    def button_clicked(self, position):
        x = int(position / self.columns)
        y = position % self.columns

        if not self.game_running:
            self.view.statusbar.showMessage("You need to restart the game!", 5000)

        try:
            n = self.model.uncover(x, y)
            button = self.grid.itemAtPosition(x, y).widget()
            label = QLabel(str(n))
            label.setStyleSheet(MinesweeperController.UNCOVERED_STYLE)
            self.grid.replaceWidget(button, label, options=Qt.FindChildrenRecursively)

            # Delete the button
            button.deleteLater()
            self.buttons.remove(button)

        except AlreadyUncoveredError:
            pass
        except FieldTaggedError:
            self.view.statusbar.showMessage("You need to untag the field before you can open it")
        except MineFound:
            self.__lose()

    def button_right_clicked(self, position):
        x = int(position / self.columns)
        y = position % self.columns

        if not self.game_running:
            self.view.statusbar.showMessage("You need to restart the game!", 5000)

        try:
            button = self.grid.itemAtPosition(x, y).widget()

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

    def __lose(self):
        # End the game
        self.game_running = False

        # Disable all buttons
        for button in self.buttons:
            button.setEnabled(False)

        # Show the mine positions:
        for x, y in self.model.mines:
            widget = self.grid.itemAtPosition(x, y).widget()
            widget.setText("\u2715")

            if self.model.field_state(x, y) == Field.COVERED:
                widget.setStyleSheet(MinesweeperController.MINE_MISSED_STYLE)
            else:
                widget.setStyleSheet(MinesweeperController.MINE_FOUND_STYLE)

        # Display a message - TODO: Open a dialog instead
        self.view.statusbar.showMessage("You lost :(", 5000)
