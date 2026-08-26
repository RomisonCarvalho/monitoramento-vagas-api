import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "vagas.db"

def conectar():
    # Garante que a pasta 'database' exista
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vagas (
            id_vaga INTEGER PRIMARY KEY AUTOINCREMENT,
            cargo_buscado TEXT,
            titulo TEXT,
            empresa TEXT,
            local TEXT,
            modelo TEXT,
            tipo_vaga TEXT,
            afirmativa_pcd TEXT,
            data TEXT,
            link TEXT UNIQUE
        )
    """)
    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    criar_tabela()