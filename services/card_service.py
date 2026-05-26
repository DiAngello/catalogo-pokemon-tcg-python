import requests
from models.carta import Carta
from models.inventario import Inventario
from repositories.carta_repo import CartaRepo
from repositories.inventario_repo import InventarioRepo
from core.database import get_conn


class CardService:

    def buscar_e_salvar(self, nome, numero, lang, qtd, extra, destino):

        numero_base = numero.split("/")[0].strip()

        cartas = requests.get(
            f"https://api.tcgdex.net/v2/{lang}/cards?name={nome}",
            timeout=10
        ).json()

        if isinstance(cartas, dict):
            cartas = cartas.get("data", [])

        if not cartas:
            raise Exception("Carta não encontrada")

        match = next(
            (c for c in cartas if str(c.get("localId","")).lstrip("0") == numero_base.lstrip("0")),
            None
        )

        if not match:
            raise Exception("Número não encontrado")

        det = requests.get(
            f"https://api.tcgdex.net/v2/{lang}/cards/{match['id']}",
            timeout=10
        ).json()

        col_id = det.get("set", {}).get("id", "unknown")
        col_nome = det.get("set", {}).get("name", "Desconhecida")

        id_carta = f"{match['id']}-{lang}"

        # AUTO cria fichário oficial
        if destino == "AUTO":
            conn = get_conn()
            conn.execute(
                "INSERT OR IGNORE INTO fichario (id_fichario, nome, is_custom) VALUES (?,?,0)",
                (col_id, col_nome)
            )
            conn.commit()
            conn.close()
            destino = col_id

        carta = Carta(
            id_carta,
            col_id,
            det.get("localId", ""),
            det.get("name", ""),
            (det.get("image") or "") + "/high.png",
            lang.upper()
        )

        CartaRepo().save(carta)

        inv = Inventario(
            None,
            id_carta,
            destino,
            qtd,
            extra
        )

        InventarioRepo().add_or_update(inv)

        return destino