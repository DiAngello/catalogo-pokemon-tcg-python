from core.database import get_conn


class InventarioRepo:

    def add_or_update(self, inv):
        conn = get_conn()
        c = conn.cursor()

        row = c.execute(
            "SELECT id_inventario, quantidade FROM inventario WHERE id_carta=? AND extras=? AND id_fichario=?",
            (inv.id_carta, inv.extras, inv.id_fichario)
        ).fetchone()

        if row:
            c.execute(
                "UPDATE inventario SET quantidade=? WHERE id_inventario=?",
                (row[1] + inv.quantidade, row[0])
            )
        else:
            c.execute(
                "INSERT INTO inventario (id_carta, quantidade, extras, id_fichario) VALUES (?,?,?,?)",
                (inv.id_carta, inv.quantidade, inv.extras, inv.id_fichario)
            )

        conn.commit()
        conn.close()

    def get_by_fichario(self, fichario_id):
        conn = get_conn()

        rows = conn.execute("""
        SELECT 
            i.id_inventario,
            c.nome,
            c.numero,
            c.imagem_url,
            c.idioma,
            i.quantidade,
            i.extras
        FROM inventario i
        JOIN carta c ON c.id_carta = i.id_carta
        WHERE i.id_fichario = ?
        ORDER BY CAST(c.numero AS INTEGER)
        """, (fichario_id,)).fetchall()

        conn.close()
        return rows