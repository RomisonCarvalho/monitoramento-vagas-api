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


def criar_tabela():
    Base.metadata.create_all(bind=engine)
