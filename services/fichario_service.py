import sqlite3


class FicharioService:

    def listar(self):
        conn = sqlite3.connect("pokemon_tcg.db")
        rows = conn.execute(
            "SELECT id_fichario, nome, is_custom FROM fichario ORDER BY nome"
        ).fetchall()
        conn.close()

        return [
            type("F", (), {
                "id_fichario": r[0],
                "nome": r[1],
                "is_custom": r[2]
            })
            for r in rows
        ]

    def deletar(self, fichario_id: str):
        conn = sqlite3.connect("pokemon_tcg.db")

        conn.execute(
            "DELETE FROM inventario WHERE id_fichario=?",
            (fichario_id,)
        )

        conn.execute(
            "DELETE FROM fichario WHERE id_fichario=?",
            (fichario_id,)
        )

        conn.commit()
        conn.close()