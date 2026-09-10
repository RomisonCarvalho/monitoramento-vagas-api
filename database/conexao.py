from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


# Carrega a configuração local do banco de dados.
# No ambiente de nuvem, DATABASE_URL é fornecida por secret.
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Interrompe a inicialização caso a conexão com o banco não esteja configurada.
if not DATABASE_URL:
    raise RuntimeError(
        "A 'DATABASE_URL' não está definida. "
        "A aplicação não pode ser iniciada sem a configuração de conexão com o banco de dados."
    )

# pool_pre_ping verifica a conexão antes de reutilizá-la,
# reduzindo falhas causadas por conexões encerradas pelo servidor.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Classe base utilizada pelos modelos ORM da aplicação.
class Base(DeclarativeBase):
    pass


def obter_sessao():
    """
    Fornece uma sessão do banco para as dependências do FastAPI
    e garante seu fechamento ao final da requisição.
    """
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()


def criar_tabela():
    """
    Cria no banco as tabelas definidas pelos modelos ORM caso ainda não existam.
    """
    Base.metadata.create_all(bind=engine)
