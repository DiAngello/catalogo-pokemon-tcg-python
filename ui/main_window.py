from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QLabel
)
from PyQt6.QtCore import Qt

from ui.components.sidebar import Sidebar
from ui.components.card_slot import CardSlot
from repositories.inventario_repo import InventarioRepo


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(1000, 650)

        root = QWidget()
        root.setObjectName("app")
        self.setCentralWidget(root)

        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)

        # ───────── Sidebar ─────────
        self.sidebar = Sidebar(self.set_fichario)
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            background-color: #1f1d2b;
            border-right: 2px solid #2e2a40;
        """)
        main_layout.addWidget(self.sidebar)

        # ───────── Página (conteúdo) ─────────
        self.page = QWidget()
        self.page.setObjectName("page")
        self.page.setStyleSheet("""
            background-color: #26233a;
            border-radius: 16px;
            padding: 20px;
        """)

        page_layout = QVBoxLayout(self.page)
        page_layout.setSpacing(15)

        # ───────── Header ─────────
        header = QHBoxLayout()

        self.title = QLabel("Selecione um fichário")
        self.title.setObjectName("title")
        self.title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #e0def4;
        """)
        header.addWidget(self.title)

        header.addStretch()

        btn_add = QPushButton("+ Adicionar carta")
        btn_add.setStyleSheet("""
            background-color: #eb6f92;
            color: white;
            padding: 6px 12px;
            border-radius: 8px;
        """)
        btn_add.clicked.connect(self.add_carta)
        header.addWidget(btn_add)

        page_layout.addLayout(header)

        # ───────── Grid ─────────
        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        page_layout.addLayout(self.grid)

        main_layout.addWidget(self.page)

        # ───────── Estado ─────────
        self.fichario_ativo = None
        self.cards = []

        self.sidebar.load()

    # ─────────────────────────────

    def set_fichario(self, fid, nome):
        self.fichario_ativo = fid
        self.title.setText(nome)
        self.load_cards()

    def load_cards(self):
        self.cards = InventarioRepo().get_by_fichario(self.fichario_ativo)
        self.render()

    # ─────────────────────────────

    def render(self):
        # limpa grid
        while self.grid.count():
            w = self.grid.takeAt(0).widget()
            if w:
                w.deleteLater()

        # estado: nenhum fichário
        if not self.fichario_ativo:
            self.show_empty("Selecione um fichário")
            return

        # estado: fichário vazio
        if not self.cards:
            self.show_empty("Nenhuma carta ainda\nClique em '+ Adicionar carta'")
            return

        # render normal
        for i in range(9):
            r, c = divmod(i, 3)
            data = self.cards[i] if i < len(self.cards) else None
            self.grid.addWidget(CardSlot(self, data), r, c)

    # ─────────────────────────────

    def show_empty(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            color: #908caa;
            font-size: 16px;
            font-weight: bold;
        """)

        self.grid.addWidget(label, 0, 0, 3, 3)

    # ─────────────────────────────

    def add_carta(self):
        from ui.dialogs.carta_dialog import CartaDialog

        dlg = CartaDialog(self)
        dlg.exec()
        
        self.sidebar.load()  
        self.load_cards()

    def edit_carta(self, data):
        from ui.dialogs.carta_dialog import CartaDialog

        dlg = CartaDialog(self, data)  # 👈 sem edit_data=
        dlg.exec()
        self.load_cards()