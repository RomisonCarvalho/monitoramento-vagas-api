from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.engine import URL
import os


load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT"))
db_name = os.getenv("DB_NAME")


class Base(DeclarativeBase):
    pass

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_name
    )

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
