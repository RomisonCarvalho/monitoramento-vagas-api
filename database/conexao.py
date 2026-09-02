import sqlite3
from pathlib import Path
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


DB_PATH = Path(__file__).resolve().parent / "vagas.db"
DATABASE_URL = "sqlite:///" + DB_PATH.as_posix()
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def obter_sessao():
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()

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
            cargo_buscado TEXT NOT NULL,
            titulo TEXT NOT NULL,
            empresa TEXT,
            local TEXT,
            modelo TEXT,
            tipo_vaga TEXT,
            afirmativa_pcd TEXT,
            data TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    criar_tabela()
