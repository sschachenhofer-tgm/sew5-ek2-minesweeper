from PyQt5.QtCore import QSignalMapper
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout

from ms_window import Ui_MainWindow
from ms_model import MinesweeperModel


class MinesweeperController(QMainWindow):
    def __init__(self, columns: int = 9, rows: int = 9, mines: int = 10):
        super().__init__(parent=None, flags=[])

        self.columns = columns
        self.rows = rows
        self.mines = mines

        # Initialize the GUI
        self.view = Ui_MainWindow()
        self.view.setupUi(self)

        # Initialize the model
        self.model = MinesweeperModel(self.columns, self.rows, mines)

        # Initialize a QSignalMapper to enable mapping all button clicks to a single method
        self.mapper = QSignalMapper(self.view)

        # Add the buttons to the GUI
        for x in range(self.columns):
            row = QVBoxLayout(self.view.columns)

            for y in range(self.rows):
                button = QPushButton(row)
                self.mapper.setMapping(button, (x, y))
                button.clicked.connect(self.mapper.ma