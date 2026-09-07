# Sistema de Monitoramento de Vagas — API

> 🚧 Projeto em desenvolvimento

API REST desenvolvida em FastAPI como evolução do projeto [Automação de Busca de Vagas com Selenium](https://github.com/RomisonCarvalho/selenium-vagas-gupy).

O projeto foi criado para transformar uma automação local de coleta de vagas em uma arquitetura distribuída, separando a busca e o tratamento dos dados da camada responsável por validação, persistência e disponibilização das informações.

## Objetivo

Disponibilizar uma API responsável por receber, validar, armazenar e consultar vagas coletadas pela automação Selenium.

A aplicação tem como objetivos:

- receber vagas enviadas pela automação por meio de requisições HTTP;
- validar os dados com Pydantic;
- persistir as informações em PostgreSQL;
- impedir o cadastro de vagas duplicadas;
- disponibilizar endpoints de consulta;
- proteger operações de escrita com API Key;
- executar em container Docker;
- disponibilizar a API em ambiente de nuvem;
- utilizar secrets externos para credenciais e configurações sensíveis.

## Arquitetura atual

```text
Automação Selenium
       ↓
 HTTPS + X-API-Key
       ↓
Google Cloud Run
       ↓
     FastAPI
       ↓
    Pydantic
       ↓
   SQLAlchemy
       ↓
     Psycopg
       ↓
Neon PostgreSQL
```

A automação e a API permanecem em repositórios separados e se comunicam exclusivamente por HTTP.

A API é empacotada em uma imagem Docker, armazenada no Google Artifact Registry e executada no Google Cloud Run. As credenciais de produção são disponibilizadas à aplicação por meio do Google Secret Manager.

## Tecnologias

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Psycopg
- PostgreSQL
- Neon
- Docker
- Docker Compose
- Google Artifact Registry
- Google Cloud Run
- Google Secret Manager
- Uvicorn
- python-dotenv
- Git / GitHub

## Dados monitorados

A API recebe os seguintes dados de cada vaga:

| Campo | Descrição |
| --- | --- |
| `cargo_buscado` | Termo utilizado pela automação na pesquisa |
| `titulo` | Título da vaga |
| `empresa` | Empresa responsável pela oportunidade |
| `localizacao` | Localização informada pela vaga |
| `modelo` | Modelo de trabalho |
| `tipo_vaga` | Tipo de contratação/oportunidade |
| `afirmativa_pcd` | Indicação de vaga também destinada a PcD |
| `data` | Data de publicação |
| `link` | Link da vaga no Gupy |

Os campos `cargo_buscado`, `titulo`, `empresa`, `data` e `link` são obrigatórios.

O `link` possui restrição de unicidade no banco de dados e é utilizado para impedir o cadastro duplicado da mesma vaga.

## Endpoints

### `GET /vagas/`

Retorna a lista de vagas cadastradas.

- acesso público;
- banco vazio retorna uma lista vazia.

### `GET /vagas/{id}`

Retorna uma vaga específica pelo identificador.

- acesso público;
- utilizado para consulta individual dos registros.

### `POST /vagas/`

Cadastra uma nova vaga.

- operação protegida por API Key;
- a chave deve ser enviada no header `X-API-Key`;
- dados recebidos são validados com Pydantic;
- duplicidades são tratadas pelo link da vaga.

Principais respostas:

| Status | Significado |
| --- | --- |
| `200` | Vaga cadastrada com sucesso |
| `401` | API Key ausente ou inválida |
| `409` | Vaga já cadastrada |
| `422` | Erro de validação dos dados enviados |

Exemplo de autenticação:

```http
X-API-Key: <sua_chave>
```

A chave real nunca deve ser armazenada no repositório.

## Validação dos dados

Os modelos Pydantic validam os campos recebidos antes da persistência.

Nos campos textuais obrigatórios:

- espaços nas extremidades são removidos;
- strings vazias não são aceitas.

As respostas da API utilizam modelos compatíveis com os objetos retornados pelo SQLAlchemy.

## Persistência

A API utiliza SQLAlchemy para comunicação com PostgreSQL.

A conexão é configurada por meio da variável de ambiente `DATABASE_URL`.

Em produção, o banco está hospedado no Neon.

O engine utiliza `pool_pre_ping=True`, permitindo que o SQLAlchemy valide conexões antes de reutilizá-las. Isso reduz falhas causadas por conexões encerradas durante períodos de inatividade em ambientes serverless.

## Segurança

O endpoint de cadastro é protegido por uma API Key compartilhada entre a automação autorizada e a API.

A aplicação:

- lê a chave esperada da variável de ambiente `API_KEY`;
- exige o header `X-API-Key` no `POST /vagas/`;
- retorna `401` quando a chave está ausente ou inválida;
- mantém os endpoints de consulta públicos.

Se `API_KEY` não estiver configurada, a aplicação não deve iniciar normalmente, evitando que o endpoint de escrita fique exposto sem autenticação.

Em produção, `DATABASE_URL` e `API_KEY` são armazenadas no Google Secret Manager e disponibilizadas ao serviço do Cloud Run em tempo de execução.

## Variáveis de ambiente

Crie um arquivo `.env` a partir do `.env.example`:

```env
DATABASE_URL=postgresql+psycopg://usuario:senha@host/banco
API_KEY=sua_chave
```

O arquivo `.env` não deve ser versionado.

Em produção, as credenciais não são incluídas na imagem Docker. Elas são fornecidas pelo ambiente de execução.

## Estrutura principal

```text
monitoramento-vagas-api/
├── api/
│   └── main.py
├── database/
│   ├── conexao.py
│   └── models.py
├── .dockerignore
├── .env.example
├── .gitignore
├── compose.yaml
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
```

A automação Selenium é mantida em um repositório separado.

## Execução local

### 1. Clone o repositório

```bash
git clone https://github.com/RomisonCarvalho/monitoramento-vagas-api.git
```

Entre na pasta:

```bash
cd monitoramento-vagas-api
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie o arquivo `.env` com base no `.env.example` e preencha:

```env
DATABASE_URL=postgresql+psycopg://usuario:senha@host/banco
API_KEY=sua_chave
```

### 5. Execute a aplicação

```bash
uvicorn api.main:app --reload
```

A documentação interativa do FastAPI ficará disponível em:

```text
http://127.0.0.1:8000/docs
```

## Docker

O projeto possui `Dockerfile` e pode ser executado de forma isolada em container.

Exemplo de build:

```bash
docker build -t monitoramento-vagas-api .
```

Exemplo de execução utilizando variáveis de ambiente de um arquivo `.env`:

```bash
docker run --env-file .env -p 8000:8000 monitoramento-vagas-api
```

O container utiliza a variável `PORT` quando fornecida pelo ambiente e assume a porta `8000` como fallback local.

## Docker Compose

Para simplificar o desenvolvimento local:

```bash
docker compose up -d --build
```

Consultar os logs:

```bash
docker compose logs -f
```

Encerrar os serviços:

```bash
docker compose down
```

## Deploy em nuvem

A imagem Docker da API é publicada no Google Artifact Registry e utilizada pelo Google Cloud Run.

Arquitetura de deploy:

```text
Código
  ↓
Docker image
  ↓
Google Artifact Registry
  ↓
Google Cloud Run
  ├── DATABASE_URL → Google Secret Manager
  └── API_KEY      → Google Secret Manager
                      ↓
                 Neon PostgreSQL
```

O serviço foi configurado para utilizar uma conta de serviço dedicada com acesso restrito aos secrets necessários.

A API pode escalar para zero instâncias durante períodos sem tráfego, reduzindo o consumo de recursos.

## Etapas do desenvolvimento

- [X] Definição do objetivo e escopo inicial
- [X] Definição da arquitetura
- [X] Criação do repositório
- [X] Introdução ao FastAPI
- [X] Criação dos endpoints
- [X] Modelagem e validação com Pydantic
- [X] Persistência com SQLAlchemy
- [X] Migração para PostgreSQL
- [X] Integração com Psycopg
- [X] Controle de duplicidade pelo link
- [X] Integração da automação com a API por HTTP
- [X] Separação entre automação e backend
- [X] Containerização com Docker
- [X] Orquestração local com Docker Compose
- [X] Banco PostgreSQL em nuvem com Neon
- [X] Publicação da imagem no Google Artifact Registry
- [X] Deploy no Google Cloud Run
- [X] Gerenciamento de credenciais com Google Secret Manager
- [X] Proteção do endpoint de escrita com `X-API-Key`
- [X] Tratamento de conexões inválidas com `pool_pre_ping`
- [X] Testes locais e em ambiente de nuvem
- [ ] Evoluções futuras de observabilidade, testes automatizados e ciclo de vida das vagas

## Status

🚧 Projeto em evolução.

A API já está funcional em ambiente de nuvem, recebe dados da automação Selenium, valida os payloads, persiste as vagas em PostgreSQL, controla duplicidades e protege operações de escrita por API Key.

As próximas evoluções poderão incluir testes automatizados, documentação adicional de respostas, observabilidade mais detalhada e mecanismos para acompanhar a disponibilidade das vagas ao longo do tempo.

## Autor

**Rômison de Jesus Carvalho**
