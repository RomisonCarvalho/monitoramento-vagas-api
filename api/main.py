from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator, ValidationInfo, ConfigDict
from datetime import date
from database.conexao import criar_tabela, obter_sessao
from database.models import VagaModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os


## 1. Configuração da aplicação

# Carrega variáveis do arquivo .env durante a execução local.
# Em nuvem, as configurações são fornecidas por variáveis de ambiente e secrets.
load_dotenv()

API_KEY = os.getenv("API_KEY")

# Impede a inicialização da aplicação sem a chave usada
# para proteger os endpoints de escrita.
if not API_KEY or not API_KEY.strip():
    raise RuntimeError("A 'API_KEY' não está definida. A aplicação não pode ser iniciada sem as credenciais de autenticação.")

def validar_api_key(api_key_header: str | None = Header(None, alias="X-API-Key")):
    """
    Valida a chave enviada no cabeçalho X-API-Key.

    Endpoints protegidos rejeitam requisições sem uma chave válida.
    """
    if api_key_header != API_KEY:
        raise HTTPException(status_code=401, detail="Acesso não autorizado: Chave de API inválida")
    

## 2. Inicialização do FastAPI

app = FastAPI()

# Disponibiliza arquivos estáticos utilizados pela interface web.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Garante a criação das tabelas definidas pelos modelos caso ainda não existam.
criar_tabela()  

## 3. Interface inicial

@app.get("/", response_class=HTMLResponse)
def pagina_inicial():
    """
    Renderiza a página inicial da aplicação com acesso à documentação
    e ao painel de consulta de vagas.
    """
    html_content = """
        <!DOCTYPE html>
        <html>
            <head> 
                <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                <title>Monitoramento de Vagas API</title>
                <link rel='stylesheet' href='/static/css/style.css'>
            </head>
            <body class='pagina-inicial'>
                <div class='card'>
                    <div class='banner'>
                        <img src="/static/images/BannerProjetoAPI.png" alt="Banner da API">
                    </div>
                    <h1>Monitoramento de Vagas API</h1>
                    <p>API desenvolvida em FastAPI para receber, validar e armazenar vagas coletadas automaticamente.</p>
                    <div class='botoes'>
                        <a href='/docs'>Documentação</a>
                        <a href='/consultar-vagas'>Consultar vagas</a>
                    </div>
                </div>                
            </body>
        </html>
    """
    return html_content



## 4. Schemas de entrada e saída

class VagaCreate(BaseModel):
    """
    Define e valida os dados necessários para cadastrar uma vaga.
    """
    cargo_buscado: str
    titulo: str
    empresa: str
    localizacao: str | None = None
    modelo: str | None = None
    tipo_vaga: str | None = None
    afirmativa_pcd: str | None = None
    data: date
    link: str

    # Remove espaços extras e impede campos obrigatórios vazios.
    @field_validator("cargo_buscado", "titulo", "empresa", "link")
    @classmethod
    def validar_nao_vazio(cls, value: str, info: ValidationInfo) -> str:
        value_stripped = value.strip()
        if not value_stripped:
            raise ValueError(f"O campo {info.field_name} não pode ser vazio ou conter apenas espaços.")
        return value_stripped


class VagaResponse(BaseModel):
    """
    Define o formato utilizado nas respostas da API.
    """

    # Permite criar a resposta diretamente a partir de objetos do SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)

    id_vaga: int
    cargo_buscado: str
    titulo: str
    empresa: str
    localizacao: str | None = None
    modelo: str | None = None
    tipo_vaga: str | None = None
    afirmativa_pcd: str | None = None
    data: date
    link: str    


## 5. Endpoints de vagas

@app.post("/vagas/", response_model=VagaResponse, dependencies=[Depends(validar_api_key)])
def armazenar_vaga(vaga: VagaCreate, sessao: Session = Depends(obter_sessao)):
    """
    Cadastra uma nova vaga no banco de dados.

    O endpoint exige autenticação por X-API-Key e retorna conflito
    quando o link da vaga já está cadastrado.
    """
    vaga_model = VagaModel(**vaga.model_dump())
    try:
        sessao.add(vaga_model)
        sessao.commit()
        sessao.refresh(vaga_model)
        return vaga_model
    except IntegrityError:
        # O link é único no banco; violações são tratadas como vaga duplicada.
        sessao.rollback()
        raise HTTPException(status_code=409, detail="Vaga já cadastrada.")


@app.get("/vagas/", response_model=list[VagaResponse])
def pegar_vagas(sessao: Session = Depends(obter_sessao)):
    """
    Retorna todas as vagas atualmente armazenadas.
    """
    consulta_vagas = select(VagaModel)
    resultado = sessao.execute(consulta_vagas)
    vagas = resultado.scalars().all()
    return vagas


## 6. Painel de consulta

@app.get("/consultar-vagas", response_class=HTMLResponse)
def pagina_consultar_vagas():
    """
    Renderiza o painel web que consulta e apresenta as vagas armazenadas pela API.
    """
    html_content = """
        <!DOCTYPE html>
        <html>
            <head> 
                <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                <title>Monitoramento de Vagas API</title>
                <link rel='stylesheet' href='/static/css/style.css'>
                <script src="/static/js/consultar-vagas.js" defer></script>
            </head>
            <body class='pagina-vagas'>
                <main class='conteudo-vagas'>
                    <h1>Painel de vagas</h1>
                    <p>Acompanhe as vagas encontradas automaticamente e explore as oportunidades já cadastradas.</p>
                    <p id='total-vagas'></p>
                    <div id='lista-vagas'>
                    </div>
                </main>               
            </body>
        </html>        
    """
    return html_content






