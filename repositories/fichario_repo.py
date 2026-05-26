import sqlite3


class FicharioRepo:

    def listar(self):
        conn = sqlite3.connect("pokemon_tcg.db")

        rows = conn.execute(
            "SELECT id_fichario, nome, is_custom FROM fichario ORDER BY nome"
        ).fetchall()

        conn.close()

        return [
            {
                "id": r[0],
                "nome": r[1],
                "is_custom": r[2]
            }
            for r in rows
        ]

    def listar_custom(self):
        conn = sqlite3.connect("pokemon_tcg.db")

        rows = conn.execute(
            "SELECT id_fichario, nome FROM fichario WHERE is_custom=1"
        ).fetchall()

        conn.close()

        return [
            {
                "id": r[0],
                "nome": r[1]
            }
            for r in rows
        ]

    def criar(self, nome):
        conn = sqlite3.connect("pokemon_tcg.db")

        import uuid
        fid = f"custom_{uuid.uuid4().hex[:8]}"

        conn.execute(
            "INSERT INTO fichario VALUES (?, ?, 1)",
            (fid, nome)
        )

        conn.commit()
        conn.close()

        return fid

    def deletar(self, fid):
        conn = sqlite3.connect("pokemon_tcg.db")

        conn.execute(
            "DELETE FROM inventario WHERE id_fichario=?",
            (fid,)
        )

        conn.execute(
            "DELETE FROM fichario WHERE id_fichario=?",
            (fid,)
        )

        conn.commit()
        conn.close()