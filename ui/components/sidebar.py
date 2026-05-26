from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt

from services.fichario_service import FicharioService
from ui.dialogs.novo_fichario_dialog import NovoFicharioDialog


class Sidebar(QWidget):

    def __init__(self, on_select):
        super().__init__()

        self.on_select = on_select
        self.setFixedWidth(220)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(6)

        self.lbl_oficial = QLabel("OFICIAL")
        self.layout.addWidget(self.lbl_oficial)

        self.list_oficial = QVBoxLayout()
        self.layout.addLayout(self.list_oficial)

        self.lbl_custom = QLabel("MEUS")
        self.layout.addWidget(self.lbl_custom)

        self.list_custom = QVBoxLayout()
        self.layout.addLayout(self.list_custom)

        self.layout.addStretch()

        self.btn_new = QPushButton("Novo fichário")
        self.btn_new.clicked.connect(self.criar_fichario)
        self.layout.addWidget(self.btn_new)

        self.buttons = []
        self.btn_delete = QPushButton("Remover fichário")
        self.btn_delete.clicked.connect(self.remover_fichario)
        self.layout.addWidget(self.btn_delete)

    def load(self):
        self.clear()

        ficharios = FicharioService().listar()

        for f in ficharios:
            btn = QPushButton(f.nome)
            btn.setProperty("fid", f.id_fichario)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            btn.clicked.connect(lambda _, b=btn: self.select(b))

            if f.is_custom:
                self.list_custom.addWidget(btn)
            else:
                self.list_oficial.addWidget(btn)

            self.buttons.append(btn)

        if self.buttons:
            self.select(self.buttons[0])

    def select(self, btn):
        fid = btn.property("fid")
    
        for b in self.buttons:
            b.setStyleSheet("")
    
        btn.setStyleSheet("background:#EB6F92; color:white;")
    
        self.current_id = fid
        self.current_name = btn.text()
    
        self.on_select(fid, btn.text())
        
        self.setStyleSheet("""
            background-color: #1f1d2b;
            border-right: 2px solid #2e2a40;
        """)

    def criar_fichario(self):
        dlg = NovoFicharioDialog(self)
        if dlg.exec():
            self.load()
            if dlg.result:
                self.on_select(dlg.result.id_fichario, dlg.result.nome)

    def clear(self):
        for layout in [self.list_oficial, self.list_custom]:
            while layout.count():
                w = layout.takeAt(0).widget()
                if w:
                    w.deleteLater()

        self.buttons.clear()
        
    def remover_fichario(self):
        if not hasattr(self, "current_id"):
            return
    
        if not self.current_id.startswith("custom_"):
            QMessageBox.warning(self, "Aviso", "Você não pode remover fichários oficiais.")
            return
    
        confirm = QMessageBox.question(
            self,
            "Remover fichário",
            f"Tem certeza que deseja remover '{self.current_name}'?\n\nTodas as cartas serão removidas.",
        )
    
        if confirm != QMessageBox.StandardButton.Yes:
            return
    
        FicharioService().deletar(self.current_id)
    
        self.load()