from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class CardSlot(QWidget):

    def __init__(self, main, data=None):
        super().__init__()

        self.main = main
        self.setFixedSize(180, 260)

        if data:
            self.build_card(data)
        else:
            self.build_empty()

    # ─────────────────────────────

    def build_empty(self):
        self.setStyleSheet("""
            background-color: #1f1d2b;
            border: 2px dashed #3a3650;
            border-radius: 12px;
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn = QPushButton("+")
        btn.setStyleSheet("""
            font-size: 28px;
            color: #6e6a86;
            border: none;
        """)
        btn.clicked.connect(self.main.add_carta)

        layout.addWidget(btn)

    # ─────────────────────────────

    def build_card(self, data):
        id_inv, nome, num, img_url, idioma, qtd, extra = data

        self.setStyleSheet("""
            background-color: #1f1d2b;
            border-radius: 12px;
            padding: 8px;
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        # imagem
        img = QLabel()
        img.setFixedSize(150, 210)
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setScaledContents(False)

        if img_url:
            px = QPixmap()
            px.loadFromData(__import__("requests").get(img_url).content)
            img.setPixmap(
                px.scaled(
                    150, 210,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

        layout.addWidget(img, alignment=Qt.AlignmentFlag.AlignCenter)

        # nome
        lbl_nome = QLabel(nome)
        lbl_nome.setWordWrap(True)
        lbl_nome.setStyleSheet("""
            color: #e0def4;
            font-size: 12px;
            font-weight: bold;
        """)
        layout.addWidget(lbl_nome)

        # número
        lbl_num = QLabel(f"#{num}")
        lbl_num.setStyleSheet("color: #908caa; font-size: 10px;")
        layout.addWidget(lbl_num)

        # quantidade
        if qtd > 1:
            lbl_qtd = QLabel(f"x{qtd}")
            lbl_qtd.setStyleSheet("color: #eb6f92; font-weight: bold;")
            layout.addWidget(lbl_qtd)

        layout.addStretch()

        # botão editar
        btn = QPushButton("Editar")
        btn.setStyleSheet("""
            background-color: #eb6f92;
            color: white;
            border-radius: 6px;
            padding: 4px;
        """)
        btn.clicked.connect(lambda: self.main.edit_carta(data))

        layout.addWidget(btn)