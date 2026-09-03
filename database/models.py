from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from database.conexao import Base
from datetime import date


class VagaModel(Base):
    __tablename__ = "vagas"
    id_vaga: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cargo_buscado: Mapped[str] = mapped_column(String, nullable=False)
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    empresa: Mapped[str] = mapped_column(String, nullable=False)
    localizacao: Mapped[str | None] = mapped_column(String)
    modelo: Mapped[str | None] = mapped_column(String)
    tipo_vaga: Mapped[str | None] = mapped_column(String)
    afirmativa_pcd: Mapped[str | None] = mapped_column(String)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    link: Mapped[str] = mapped_column(String, unique=True, nullable=False)

