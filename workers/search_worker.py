from PyQt6.QtCore import QThread, pyqtSignal
from services.card_service import CardService

class SearchWorker(QThread):
    success = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, nome, numero, lang, qtd, extra, destino):
        super().__init__()
        self.nome = nome
        self.numero = numero
        self.lang = lang
        self.qtd = qtd
        self.extra = extra
        self.destino = destino

    def run(self):
        try:
            service = CardService()
            res = service.buscar_e_salvar(
                self.nome, self.numero, self.lang,
                self.qtd, self.extra, self.destino
            )
            self.success.emit(res)
        except Exception as e:
            self.error.emit(str(e))