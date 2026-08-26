from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel, field_validator, ValidationInfo
from datetime import date
from database.conexao import criar_tabela, conectar
import sqlite3

app = FastAPI()
criar_tabela()  


class Vaga(BaseModel):
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

@app.post("/vagas/")
def armazenar_vaga(vaga: Vaga):
    print(f"Vaga recebida: {vaga}")
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO vagas (
            cargo_buscado, titulo, empresa, local, modelo, 
            tipo_vaga, afirmativa_pcd, data, link
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    valores = (
        vaga.cargo_buscado,
        vaga.titulo,
        vaga.empresa,
        vaga.local,
        vaga.modelo,
        vaga.tipo_vaga,
        vaga.afirmativa_pcd,
        vaga.data.isoformat(),
        vaga.link
    )
    try:
        cursor.execute(sql, valores)
        conexao.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Essa vaga já foi cadastrada anteriormente (link duplicado)."
        )
    finally:
        conexao.close()
    return vaga.model_dump()


@app.get("/vagas/")
def pegar_vagas():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM vagas")
    colunas = [col[0] for col in cursor.description]
    linhas = cursor.fetchall()
    vagas = [dict(zip(colunas, linha)) for linha in linhas]
    
    conexao.close()
    
    return vagas