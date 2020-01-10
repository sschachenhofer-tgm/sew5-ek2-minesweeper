from PyQt5.QtCore import QSignalMapper, Qt
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout

from ms_window import Ui_MainWindow
from ms_model import MinesweeperModel, MineFound, AlreadyUncoveredError


class MinesweeperController(QMainWindow):
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

        # Add the buttons to the GUI
        grid = QGridLayout()
        self.view.main_layout.addLayout(grid)
        grid.setSpacing(5)

        # This is the only way to keep a reference to all buttons on the board, since buttons are "re-parented" to the
        # main window after being added to a layout
        self.buttons = []

        for n in range(self.columns * self.rows):
            button = QPushButton()
            button.setFixedSize(40, 40)
            self.mapper.setMapping(button, n)
            button.clicked.connect(self.mapper.map)

            grid.addWidget(button, int(n / self.columns), n % self.columns, alignment=Qt.AlignCenter)
            self.buttons.append(button)

        # Resize the rows
        for i in range(grid.rowCount()):
            grid.setRowMinimumHeight(i, 30)

        # Resize the columns
        for i in range(grid.columnCount()):
            grid.setColumnMinimumWidth(i, 30)

        grid.setSizeConstraint(QGridLayout.SetFixedSize)

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

        except AlreadyUncoveredError:
            pass
        except MineFound:
            self.__lose()

    def __lose(self):
        # End the game
        self.game_running = False

        # Disable all buttons
        for button in self.buttons:
            button.setEnabled(False)

        # Display a message - TODO: Open a dialog instead
        self.view.statusbar.showMessage("You lost :(", 5000)
