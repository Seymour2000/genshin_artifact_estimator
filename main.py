from PyQt6 import QtWidgets
from ui import UI
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())