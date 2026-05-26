import requests
import sqlite3
from repositories.fichario_repo import FicharioRepo
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QSpinBox, QMessageBox
)


class CartaDialog(QDialog):

    def __init__(self, parent=None, edit_data=None):
        super().__init__(parent)

        self.edit_data = edit_data
        self.setFixedSize(320, 400)

        self.layout = QVBoxLayout(self)

        if edit_data:
            self.build_edit()
        else:
            self.build_add()

    # ─────────────────────────
    # ADICIONAR CARTA
    # ─────────────────────────
    def build_add(self):
        self.layout.addWidget(QLabel("Adicionar carta"))
    
        # destino
        self.cb_destino = QComboBox()
        self.cb_destino.addItem("Coleção original (automático)", "AUTO")
    
        ficharios = FicharioRepo().listar_custom()
    
        for f in ficharios:
            self.cb_destino.addItem(f["nome"], f["id"])
    
        self.layout.addWidget(self.cb_destino)
    
        self.inp_nome = QLineEdit()
        self.inp_nome.setPlaceholderText("Nome da carta")
        self.layout.addWidget(self.inp_nome)
    
        self.inp_num = QLineEdit()
        self.inp_num.setPlaceholderText("Número")
        self.layout.addWidget(self.inp_num)
    
        self.cb_lang = QComboBox()
        self.cb_lang.addItem("Português", "pt")
        self.cb_lang.addItem("Inglês", "en")
        self.cb_lang.addItem("Japonês", "ja")
        self.layout.addWidget(self.cb_lang)
    
        self.spin_qtd = QSpinBox()
        self.spin_qtd.setValue(1)
        self.layout.addWidget(self.spin_qtd)
    
        self.cb_extra = QComboBox()
        self.cb_extra.addItems([
            "Normal", "Foil", "Reverse Foil", "Promo"
        ])
        self.layout.addWidget(self.cb_extra)
    
        btn = QPushButton("Buscar e adicionar")
        btn.clicked.connect(self.buscar)
        self.layout.addWidget(btn)

    def buscar(self):
        nome = self.inp_nome.text().strip()
        numero = self.inp_num.text().strip()
        lang = self.cb_lang.currentData()

        if not nome or not numero:
            QMessageBox.warning(self, "Aviso", "Preencha nome e número")
            return

        try:
            res = requests.get(
                f"https://api.tcgdex.net/v2/{lang}/cards?name={nome}",
                timeout=10
            ).json()

            if isinstance(res, dict):
                res = res.get("data", [])

            if not res:
                raise Exception("Carta não encontrada")

            numero_base = numero.split("/")[0]

            match = next(
                (c for c in res if c.get("localId") == numero_base),
                None
            )

            if not match:
                raise Exception("Número não encontrado")

            det = requests.get(
                f"https://api.tcgdex.net/v2/{lang}/cards/{match['id']}",
                timeout=10
            ).json()

            self.salvar(det, lang)

        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def salvar(self, det, lang):
        nome = det.get("name")
        num = det.get("localId")
        col_id = det.get("set", {}).get("id", "unknown")
        col_nome = det.get("set", {}).get("name", "Coleção")
    
        img = det.get("image")
        if img:
            img = img + "/high.png"
    
        id_carta = f"{det['id']}-{lang}"
    
        destino = self.cb_destino.currentData()
    
        conn = sqlite3.connect("pokemon_tcg.db")
        c = conn.cursor()
    
        # salva carta
        c.execute(
            "INSERT OR IGNORE INTO carta VALUES (?,?,?,?,?,?)",
            (id_carta, col_id, num, nome, img, lang.upper())
        )
    
        # decide fichário
        if destino == "AUTO":
            if not col_id or col_id == "unknown":
                col_id = f"auto_{det['id']}"
                col_nome = "Coleção desconhecida"
        
            c.execute(
                "INSERT OR IGNORE INTO fichario (id_fichario, nome, is_custom) VALUES (?, ?, 0)",
                (col_id, col_nome)
            )
        
            destino_final = col_id
        else:
            destino_final = destino
    
        # inventário (evita duplicar)
        row = c.execute(
            "SELECT id_inventario, quantidade FROM inventario WHERE id_carta=? AND extras=? AND id_fichario=?",
            (id_carta, self.cb_extra.currentText(), destino_final)
        ).fetchone()
    
        if row:
            c.execute(
                "UPDATE inventario SET quantidade=? WHERE id_inventario=?",
                (row[1] + self.spin_qtd.value(), row[0])
            )
        else:
            c.execute(
                "INSERT INTO inventario (id_carta, quantidade, extras, id_fichario) VALUES (?,?,?,?)",
                (id_carta, self.spin_qtd.value(), self.cb_extra.currentText(), destino_final)
            )
    
        conn.commit()
        conn.close()
    
        self.accept()

    # ─────────────────────────
    # EDITAR CARTA
    # ─────────────────────────
    def build_edit(self):
        id_inv, nome, num, _, idioma, qtd, extra = self.edit_data

        self.layout.addWidget(QLabel(f"{nome} • #{num} • {idioma}"))

        self.spin_qtd = QSpinBox()
        self.spin_qtd.setValue(qtd)
        self.layout.addWidget(self.spin_qtd)

        self.cb_extra = QComboBox()
        self.cb_extra.addItems(["Normal", "Foil", "Reverse Foil", "Promo"])
        self.cb_extra.setCurrentText(extra)
        self.layout.addWidget(self.cb_extra)

        btn_save = QPushButton("Salvar")
        btn_save.clicked.connect(lambda: self.save(id_inv))
        self.layout.addWidget(btn_save)

        btn_delete = QPushButton("Remover")
        btn_delete.clicked.connect(lambda: self.delete(id_inv))
        self.layout.addWidget(btn_delete)

    def save(self, id_inv):
        conn = sqlite3.connect("pokemon_tcg.db")
        conn.execute(
            "UPDATE inventario SET quantidade=?, extras=? WHERE id_inventario=?",
            (self.spin_qtd.value(), self.cb_extra.currentText(), id_inv)
        )
        conn.commit()
        conn.close()
        self.accept()

    def delete(self, id_inv):
        conn = sqlite3.connect("pokemon_tcg.db")
        conn.execute(
            "DELETE FROM inventario WHERE id_inventario=?",
            (id_inv,)
        )
        conn.commit()
        conn.close()
        self.accept()