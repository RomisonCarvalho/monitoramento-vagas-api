from fastapi import FastAPI, Depends
from fastapi import HTTPException
from pydantic import BaseModel, field_validator, ValidationInfo, ConfigDict
from datetime import date
from database.conexao import criar_tabela, conectar, obter_sessao
from database.models import VagaModel
import sqlite3
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

app = FastAPI()
criar_tabela()  


class VagaCreate(BaseModel):
    cargo_buscado: str
    titulo: str
    empresa: str
    local: str | None = None
    modelo: str | None = None
    tipo_vaga: str | None = None
    afirmativa_pcd: str | None = None
    data: date
    link: str

    @field_validator("cargo_buscado", "titulo", "empresa", "link")
    @classmethod
    def validar_nao_vazio(cls, value: str, info: ValidationInfo) -> str:
        value_stripped = value.strip()
        if not value_stripped:
            raise ValueError(f"O campo {info.field_name} não pode ser vazio ou conter apenas espaços.")
        return value_stripped


class VagaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_vaga: int
    cargo_buscado: str
    titulo: str
    empresa: str
    local: str | None = None
    modelo: str | None = None
    tipo_vaga: str | None = None
    afirmativa_pcd: str | None = None
    data: date
    link: str    


@app.post("/vagas/", response_model=VagaResponse)
def armazenar_vaga(vaga: VagaCreate, sessao: Session = Depends(obter_sessao)):
    vaga_model = VagaModel(**vaga.model_dump())
    try:
        sessao.add(vaga_model)
        sessao.commit()
        sessao.refresh(vaga_model)
        return vaga_model
    except IntegrityError:
        sessao.rollback()
        raise HTTPException(status_code=409, detail="Vaga já cadastrada.")


    # print(f"Vaga recebida: {vaga}")
    # conexao = conectar()
    # cursor = conexao.cursor()

    # sql = """
    #     INSERT INTO vagas (
    #         cargo_buscado, titulo, empresa, local, modelo, 
    #         tipo_vaga, afirmativa_pcd, data, link
    #     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    # """
    # valores = (
    #     vaga.cargo_buscado,
    #     vaga.titulo,
    #     vaga.empresa,
    #     vaga.local,
    #     vaga.modelo,
    #     vaga.tipo_vaga,
    #     vaga.afirmativa_pcd,
    #     vaga.data.isoformat(),
    #     vaga.link
    # )

    # try:
    #     cursor.execute(sql, valores)
    #     conexao.commit()
    # except sqlite3.IntegrityError:
    #     raise HTTPException(
    #         status_code=409,
    #         detail="Essa vaga já foi cadastrada anteriormente (link duplicado)."
    #     )
    # finally:
    #     conexao.close()
    # return vaga.model_dump()


@app.get("/vagas/", response_model=list[VagaResponse])
def pegar_vagas(sessao: Session = Depends(obter_sessao)):
    consulta_vagas = select(VagaModel)
    resultado = sessao.execute(consulta_vagas)
    vagas = resultado.scalars().all()
    return vagas
  





