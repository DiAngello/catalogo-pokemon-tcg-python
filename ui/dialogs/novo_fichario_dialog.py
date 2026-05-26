from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton
from services.fichario_service import FicharioService


class NovoFicharioDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.nome = QLineEdit()
        self.layout.addWidget(self.nome)

        btn = QPushButton("Criar")
        btn.clicked.connect(self.criar)
        self.layout.addWidget(btn)

        self.result = None

    def criar(self):
        service = FicharioService()
        self.result = service.criar(self.nome.text())
        self.accept()