from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
import requests

_cache = {}

class ImageLoader(QThread):
    loaded = pyqtSignal(str, QPixmap)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        if self.url in _cache:
            self.loaded.emit(self.url, _cache[self.url])
            return

        try:
            data = requests.get(self.url).content
            px = QPixmap()
            px.loadFromData(data)
            _cache[self.url] = px
            self.loaded.emit(self.url, px)
        except:
            self.loaded.emit(self.url, QPixmap())