import sqlite3

DB_NAME = "pokemon_tcg.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = sqlite3.connect("pokemon_tcg.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS fichario (
        id_fichario TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        is_custom INTEGER DEFAULT 0
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS carta (
        id_carta TEXT PRIMARY KEY,
        id_colecao TEXT,
        numero TEXT,
        nome TEXT,
        imagem_url TEXT,
        idioma TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS inventario (
        id_inventario INTEGER PRIMARY KEY AUTOINCREMENT,
        id_carta TEXT,
        id_fichario TEXT,
        quantidade INTEGER,
        extras TEXT
    )""")

    exists = c.execute("SELECT COUNT(*) FROM fichario").fetchone()[0]

    if exists == 0:
        c.execute("""
            INSERT INTO fichario VALUES
            ('demo', 'Meu primeiro fichário', 1)
        """)

    conn.commit()
    conn.close()