import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from core.database import init_db
from ui.main_window import MainWindow

def main():
    init_db()

    app = QApplication(sys.argv)

    with open("assets/style.qss") as f:
        app.setStyleSheet(f.read())

    app.setWindowIcon(QIcon("assets/icon.ico"))

    win = MainWindow()
    win.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()