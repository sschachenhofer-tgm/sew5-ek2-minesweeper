import sys

from PyQt5.QtWidgets import QApplication

from ms_controller import MinesweeperController

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] in ["-h", "--help"]:
        print("You can specify the number of width and height of the field and the number of mines to place:")
        print("python minesweeper.py <width> <height> <number of mines>")
        sys.exit(-1)

    app = QApplication([])

    if len(sys.argv) >= 4:
        window = MinesweeperController(columns=int(sys.argv[1]), rows=int(sys.argv[2]), mines=int(sys.argv[3]))
    else:
        window = MinesweeperController()

    window.show()
    sys.exit(app.exec())
