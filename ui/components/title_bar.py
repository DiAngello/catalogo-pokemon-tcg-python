from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt


class TitleBar(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        layout = QHBoxLayout(self)

        layout.addWidget(QLabel("pokemon diary"))

        layout.addStretch()

        btn_min = QPushButton("-")
        btn_min.clicked.connect(parent.showMinimized)
        layout.addWidget(btn_min)

        btn_close = QPushButton("x")
        btn_close.clicked.connect(parent.close)
        layout.addWidget(btn_close)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.window().windowHandle().startSystemMove()