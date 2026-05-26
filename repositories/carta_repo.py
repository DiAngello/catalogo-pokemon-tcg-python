from core.database import get_conn
from models.carta import Carta


class CartaRepo:

    def save(self, carta: Carta):
        conn = get_conn()
        conn.execute(
            "INSERT OR IGNORE INTO carta VALUES (?,?,?,?,?,?)",
            carta.to_tuple()
        )
        conn.commit()
        conn.close()

    def get_all(self):
        conn = get_conn()
        rows = conn.execute("SELECT * FROM carta").fetchall()
        conn.close()

        return [Carta.from_row(r) for r in rows]