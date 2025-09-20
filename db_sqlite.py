import sqlite3
from sqlite3 import Connection
from typing import List, Optional, Dict

DB_FILE = "dados.sqlite3"

def criar_conexao_sqlite(db_file: str = DB_FILE) -> Connection:
    """Create and return a sqlite3 connection."""
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas(conn: Connection):
    """Create estados and cidades tables if not exist."""
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS estados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        estado_id INTEGER,
        FOREIGN KEY (estado_id) REFERENCES estados(id)
    )
    """)
    conn.commit()

def inserir_estado(conn: Connection, nome: str) -> int:
    """Insert state if not exists and return its id."""
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO estados (nome) VALUES (?)", (nome,))
    conn.commit()
    cur.execute("SELECT id FROM estados WHERE nome = ?", (nome,))
    row = cur.fetchone()
    return row["id"]

def inserir_cidade(conn: Connection, nome: str, estado_id: int) -> int:
    """Insert a city and return the new id."""
    cur = conn.cursor()
    cur.execute("INSERT INTO cidades (nome, estado_id) VALUES (?, ?)", (nome, estado_id))
    conn.commit()
    return cur.lastrowid

def listar_cidades(conn: Connection) -> List[Dict]:
    """Return list of cities with their state names."""
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.nome as cidade, e.nome as estado
        FROM cidades c LEFT JOIN estados e ON c.estado_id = e.id
        ORDER BY e.nome, c.nome
    """)
    return [dict(row) for row in cur.fetchall()]

def buscar_cidade_por_nome(conn: Connection, nome: str) -> Optional[Dict]:
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM cidades WHERE nome = ?", (nome,))
    row = cur.fetchone()
    return dict(row) if row else None

if __name__ == "__main__":
    conn = criar_conexao_sqlite()
    criar_tabelas(conn)
    print("SQLite ready")
