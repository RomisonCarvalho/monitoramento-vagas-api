# Sistema de Monitoramento de Vagas — API

API REST desenvolvida em FastAPI como evolução do projeto [Automação de Busca de Vagas com Selenium](https://github.com/RomisonCarvalho/selenium-vagas-gupy).

O projeto separa a coleta de vagas da camada responsável por validação, persistência e disponibilização das informações. A automação e a API são mantidas em repositórios independentes e se comunicam por HTTP.

## Objetivo

Disponibilizar um backend responsável por receber, validar, armazenar e consultar vagas coletadas automaticamente.

A aplicação:

- recebe vagas enviadas pela automação por requisições HTTP;
- valida os dados com Pydantic;
- persiste as informações em PostgreSQL;
- impede o cadastro duplicado da mesma vaga pelo link;
- disponibiliza consulta pública das vagas armazenadas;
- protege operações de escrita com API Key;
- disponibiliza uma interface web para consulta das oportunidades;
- executa em container Docker;
- está implantada no Google Cloud Run;
- utiliza secrets externos para credenciais e configurações sensíveis.

## Arquitetura atual

```text
Automação Selenium
(repositório separado / Cloud Run Job)
              ↓
       HTTPS + X-API-Key
              ↓
     Google Cloud Run
              ↓
           FastAPI
          ↙       ↘
 Interface web   Pydantic
                    ↓
               SQLAlchemy
                    ↓
                 Psycopg
                    ↓
             Neon PostgreSQL
```

A API é empacotada em uma imagem Docker, armazenada no Google Artifact Registry e executada como serviço no Google Cloud Run.

Na execução em nuvem, `DATABASE_URL` e `API_KEY` são fornecidas pelo Google Secret Manager. O banco PostgreSQL utilizado pela aplicação está hospedado no Neon.

## Tecnologias

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Psycopg
- PostgreSQL
- Neon
- Uvicorn
- HTML
- CSS
- JavaScript
- Docker
- Docker Compose
- Google Artifact Registry
- Google Cloud Run
- Google Secret Manager
- python-dotenv
- Git / GitHub

## Dados monitorados

A API recebe os seguintes dados de cada vaga:

| Campo              | Descrição                                  |
| ------------------ | -------------------------------------------- |
| `cargo_buscado`  | Termo utilizado pela automação na pesquisa |
| `titulo`         | Título da vaga                              |
| `empresa`        | Empresa responsável pela oportunidade       |
| `localizacao`    | Localização informada pela vaga            |
| `modelo`         | Modelo de trabalho                           |
| `tipo_vaga`      | Tipo de contratação/oportunidade           |
| `afirmativa_pcd` | Indicação de vaga também destinada a PcD  |
| `data`           | Data de publicação                         |
| `link`           | Link da vaga no Gupy                         |

Os campos `cargo_buscado`, `titulo`, `empresa`, `data` e `link` são obrigatórios.

Os campos textuais obrigatórios têm os espaços nas extremidades removidos e não aceitam strings vazias ou compostas apenas por espaços.

O campo `link` possui restrição de unicidade no banco e funciona como controle de duplicidade.

## Endpoints

### `GET /`

Renderiza a página inicial da aplicação, com acesso à documentação interativa e ao painel de vagas.

### `GET /consultar-vagas`

Renderiza o painel web de consulta.

O painel:

- consulta os dados pelo endpoint `GET /vagas/`;
- exibe o total de vagas atualmente cadastradas;
- organiza as oportunidades pelo cargo utilizado na busca;
- ordena as vagas pela data de publicação;
- apresenta os dados em cards;
- disponibiliza acesso ao link original da oportunidade.

### `GET /vagas/`

Retorna a lista de vagas cadastradas.

- acesso público;
- banco vazio retorna uma lista vazia.

### `POST /vagas/`

Cadastra uma nova vaga.

- operação protegida por API Key;
- a chave deve ser enviada no header `X-API-Key`;
- os dados recebidos são validados com Pydantic;
- duplicidades são tratadas pela restrição de unicidade do link.

Principais respostas:

| Status  | Significado                            |
| ------- | -------------------------------------- |
| `200` | Vaga cadastrada com sucesso            |
| `401` | API Key ausente ou inválida           |
| `409` | Vaga já cadastrada                    |
| `422` | Erro de validação dos dados enviados |

Exemplo de autenticação:

```http
X-API-Key: <sua_chave>
```

A chave real nunca deve ser armazenada no repositório.

## Validação dos dados

O schema de entrada valida os dados antes da persistência.

Nos campos textuais obrigatórios:

- espaços nas extremidades são removidos;
- strings vazias não são aceitas;
- strings contendo apenas espaços também não são aceitas.

As respostas utilizam um schema compatível com os objetos retornados pelo SQLAlchemy.

## Persistência

A API utiliza SQLAlchemy para comunicação com PostgreSQL por meio do driver Psycopg.

A conexão é configurada pela variável de ambiente `DATABASE_URL`.

Antes de criar o engine, a aplicação verifica se `DATABASE_URL` foi configurada. Sem uma URL válida, a inicialização é interrompida com uma mensagem explícita.

O engine utiliza `pool_pre_ping=True`, permitindo que o SQLAlchemy valide conexões antes de reutilizá-las. Isso reduz falhas causadas por conexões encerradas durante períodos de inatividade em ambientes serverless.

## Segurança

O endpoint de cadastro é protegido por uma API Key compartilhada entre a automação autorizada e a API.

A aplicação:

- lê a chave esperada da variável de ambiente `API_KEY`;
- rejeita a inicialização se a configuração estiver ausente ou vazia;
- exige o header `X-API-Key` no `POST /vagas/`;
- retorna `401` quando a chave enviada está ausente ou inválida;
- mantém as rotas de consulta públicas.

Na execução em nuvem, `DATABASE_URL` e `API_KEY` são armazenadas no Google Secret Manager e disponibilizadas ao serviço do Cloud Run em tempo de execução.

## Variáveis de ambiente

Crie um arquivo `.env` a partir do `.env.example`:

```env
DATABASE_URL=postgresql+psycopg://usuario:senha@host:5432/nome_do_banco
API_KEY=sua_chave
```

O arquivo `.env` não deve ser versionado.

A aplicação utiliza `python-dotenv` para carregar essas variáveis localmente. Na execução em nuvem, as credenciais não são incluídas na imagem Docker.

## Estrutura principal

```text
monitoramento-vagas-api/
├── api/
│   └── main.py
├── database/
│   ├── conexao.py
│   └── models.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   └── BannerProjetoAPI.png
│   └── js/
│       └── consultar-vagas.js
├── .dockerignore
├── .env.example
├── .gitignore
├── compose.yaml
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
```

A automação Selenium é mantida no repositório [selenium-vagas-gupy](https://github.com/RomisonCarvalho/selenium-vagas-gupy).

## Execução local

### 1. Clone o repositório

```bash
git clone https://github.com/RomisonCarvalho/monitoramento-vagas-api.git
cd monitoramento-vagas-api
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie o arquivo `.env` com base no `.env.example` e preencha `DATABASE_URL` e `API_KEY`.

### 5. Execute a aplicação

```bash
python -m uvicorn api.main:app --reload
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000
```

Documentação interativa:

```text
http://127.0.0.1:8000/docs
```

Painel de vagas:

```text
http://127.0.0.1:8000/consultar-vagas
```

## Docker

O projeto possui `Dockerfile` e pode ser executado de forma isolada em container.

Build da imagem:

```bash
docker build -t monitoramento-vagas-api .
```

Execução utilizando as variáveis de um arquivo `.env`:

```bash
docker run --env-file .env -p 8000:8000 monitoramento-vagas-api
```

O container utiliza a variável `PORT` quando fornecida pelo ambiente e assume a porta `8000` como fallback local.

## Docker Compose

Para simplificar a execução local em container:

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

## Execução em nuvem

Na versão atual, a imagem Docker da API é armazenada no Google Artifact Registry e utilizada pelo Google Cloud Run.

```text
Código
  ↓
Imagem Docker
  ↓
Google Artifact Registry
  ↓
Google Cloud Run
  ├── DATABASE_URL → Google Secret Manager
  └── API_KEY      → Google Secret Manager
                      ↓
                 Neon PostgreSQL
```

O serviço utiliza uma conta de serviço dedicada com acesso restrito aos secrets necessários.

A configuração permite escalar para zero instâncias durante períodos sem tráfego, reduzindo o consumo de recursos.

## Evolução do projeto

O desenvolvimento passou pelas seguintes etapas:

- definição do objetivo e da arquitetura;
- criação dos endpoints e schemas Pydantic;
- persistência inicialmente estudada e posteriormente estruturada com SQLAlchemy;
- migração da persistência para PostgreSQL no Neon;
- integração com Psycopg;
- controle de duplicidade pelo link;
- integração da automação e da API por HTTP;
- separação da automação e do backend em repositórios independentes;
- proteção do endpoint de escrita com `X-API-Key`;
- criação da interface web para consulta das vagas;
- adição do contador de oportunidades cadastradas;
- containerização com Docker e Docker Compose;
- publicação da imagem no Google Artifact Registry;
- deploy da API no Google Cloud Run;
- gerenciamento de credenciais com Google Secret Manager;
- configuração de `pool_pre_ping` para conexões em ambiente serverless;
- testes locais e em ambiente de nuvem.

## Possíveis evoluções futuras

O projeto foi concluído dentro do escopo definido. Evoluções futuras podem ser adicionadas como novos estudos, sem fazer parte dos requisitos da versão atual, por exemplo:

- testes automatizados;
- observabilidade mais detalhada;
- filtros e paginação no painel;
- acompanhamento do ciclo de vida das vagas.

## Status

✅ **Projeto concluído dentro do escopo definido.**

A versão atual está funcional em ambiente de nuvem, recebe dados da automação Selenium, valida os payloads, persiste as vagas em PostgreSQL, controla duplicidades, protege operações de escrita por API Key e disponibiliza um painel web para consulta das oportunidades cadastradas.

## Autor

**Rômison de Jesus Carvalho**
