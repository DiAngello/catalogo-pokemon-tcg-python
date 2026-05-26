import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from core.database import init_db
from ui.main_window import MainWindow


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def main():
    init_db()

    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(resource_path("assets/icon.ico")))

    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()