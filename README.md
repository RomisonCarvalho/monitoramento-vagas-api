# Sistema de Monitoramento de Vagas com Automação e API

> 🚧 Projeto em desenvolvimento

Evolução do projeto [Automação de Busca de Vagas com Selenium](https://github.com/RomisonCarvalho/selenium-vagas-gupy), criado para automatizar a busca de oportunidades no Gupy.

Neste novo projeto, a automação será expandida para uma aplicação composta por automação web, API REST, banco de dados e notificações, com foco em praticar conceitos de backend e integração entre serviços.

## Objetivo

Transformar a automação de busca de vagas em um sistema de monitoramento capaz de:

- pesquisar vagas no Gupy utilizando Selenium;
- coletar e tratar as informações encontradas;
- enviar os dados para uma API desenvolvida em FastAPI;
- armazenar o histórico das vagas em PostgreSQL;
- evitar o armazenamento de vagas duplicadas;
- manter logs das execuções;
- enviar uma notificação por e-mail ao final da execução;
- disponibilizar a aplicação em ambiente de nuvem.

## Evolução do projeto

### Projeto anterior

```text
Gupy → Selenium → tratamento dos dados → CSV → logs
```

### Novo projeto

```text
Gupy → Selenium → FastAPI → PostgreSQL
                         ├── logs
                         └── e-mail
```

A automação existente será utilizada como base para a nova aplicação, preservando a lógica de busca, paginação, filtragem por trabalho remoto, tratamento de dados e controle de duplicidade já desenvolvidos no projeto anterior.

## Dados monitorados

A primeira versão do sistema utilizará os mesmos dados coletados pela automação anterior:

- Cargo buscado
- Título da vaga
- Empresa
- Local
- Modelo de trabalho
- Tipo da vaga
- Afirmativa para PcD
- Data de publicação
- Link da vaga

O `Link` será utilizado como identificador da vaga para evitar duplicidades.

## Tecnologias planejadas

- Python
- Selenium
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Git / GitHub
- Serviço de hospedagem em nuvem

## Estrutura inicial

```text
monitoramento-vagas-api/
├── automacao/
├── api/
├── database/
├── logs/
├── tests/
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

A estrutura será ajustada conforme as responsabilidades de cada componente forem definidas durante o desenvolvimento.

## Etapas do desenvolvimento

- [X] Definição do objetivo e escopo inicial
- [X] Definição da arquitetura inicial
- [X] Criação do novo repositório no GitHub
- [X] Estrutura inicial do projeto
- [ ] Definição das responsabilidades de cada componente
- [ ] Introdução ao FastAPI
- [ ] Criação dos primeiros endpoints
- [ ] Modelagem dos dados
- [ ] Integração com PostgreSQL
- [ ] Integração da automação com a API
- [ ] Implementação das regras de duplicidade
- [ ] Implementação e aprimoramento dos logs
- [ ] Implementação das notificações por e-mail
- [ ] Testes
- [ ] Deploy da API
- [ ] Configuração do banco de dados em nuvem
- [ ] Execução automatizada em ambiente de nuvem

## Status

🚧 Em desenvolvimento.

Este projeto está sendo construído como uma evolução prática de um projeto anterior de automação com Selenium, com o objetivo de aprofundar conhecimentos em automação, APIs, persistência de dados, backend e cloud.

## Autor

**Rômison de Jesus Carvalho**
