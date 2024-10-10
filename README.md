# NPS Survey System

![NPS Survey](https://img.shields.io/badge/license-MIT-blue.svg)

## 🧐 Sobre

O **NPS Survey System** é uma aplicação desenvolvida em Django que permite a criação e gerenciamento de pesquisas de Net Promoter Score (NPS). O sistema facilita o processo de criação de usuários, questões, formulários de pesquisa e a coleta de respostas dos respondentes. Além disso, inclui funcionalidades de autenticação segura e disparo de e-mails para convites às pesquisas.

## 🚀 Funcionalidades

- **Autenticação Segura:** Utiliza tokens para proteger endpoints e garantir que apenas usuários autorizados possam acessar recursos sensíveis.
- **Gerenciamento de Usuários:** Cadastro e gerenciamento de usuários através do painel admin do Django.
- **Criação de Questões Diversificadas:** Suporta questões de texto livre, respostas binárias (Sim/Não) e avaliações de 1 a 10.
- **Formulários de Pesquisa Personalizáveis:** Criação de formulários de pesquisa que podem ser atribuídos com diferentes questões.
- **Coleta e Armazenamento de Respostas:** Armazena respostas detalhadas, associando cada resposta a um respondente e ao formulário correspondente.
- **Disparo de E-mails:** Envio de convites para participação nas pesquisas diretamente do painel admin, restrito a usuários superadmin.
- **API RESTful:** Fornece endpoints para interação com o sistema de forma programática.

## 🛠️ Instalação

### 🔧 Pré-requisitos

Antes de iniciar, certifique-se de ter o seguinte instalado em sua máquina:

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (opcional, mas recomendado)

### 📦 Passo a Passo

1. **Clone o Repositório**

```bash
    git clone https://github.com/PedroHLV/NPS_DJANGO.git
    cd nps_project
```
2. **Crie um Ambiente Virtual**
```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/MacOS
    venv\Scripts\activate     # Para Windows
```
3. **Instale as Dependências**
```bash
    pip install -r requirements.txt
```
4. **Configure as Variaveis de Ambiente**
```bash
    EMAIL_HOST=
    EMAIL_PORT=
    EMAIL_HOST_USER=
    EMAIL_HOST_PASSWORD=
    EMAIL_USE_TLS=True
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```
5. **Aplique as Migrações**
```bash
    python manage.py makemigrations
    python manage.py migrate
```
6. **Crie um Superusuário**
```bash
    python manage.py createsuperuser
```
6. **Execute o servidor**
```bash
    python manage.py runserver
```

## 🖥️ Uso
**🔑 Autenticação:**
Para interagir com os endpoints protegidos da API, é necessário obter um token de autenticação. Siga os passos abaixo:
1. **Obtenha o Token:** Faça uma requisição POST para a rota /api-token-auth/ passando username e password de um usuário cadastrado no Django Admin.
```json
POST http://127.0.0.1:8000/api-token-auth/

Corpo da Requisição:
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```
1. **Utilize o Token nas Requisições:** Inclua o token no cabeçalho de autorização de suas requisições para acessar os endpoints protegidos.

    Exemplo de Cabeçalho
```json
Authorization: Token seu_token_aqui
```
## 🛡️ Painel Admin
Acesse o painel admin do Django para gerenciar usuários, questões, formulários e mais.

URL do Admin: http://127.0.0.1:8000/admin/

Credenciais: Utilize o superusuário criado durante a instalação.

## 🔄 Fluxo do Sistema
1. **Cadastro de Usuários:** 
    - Crie e gerencie usuários através do painel admin do Django
2. **Criação de Questões:** 
    - Adicione questões independentes que podem ser de três tipos:
    - Texto Livre: Permite respostas abertas.
    - Sim/Não: Respostas Binárias.
    - Nota (1-10): Avaliação numéricas com opções clicáveis.
3. **Criação de Formulários de Pesquisa:**
    - Crie formulários (Surveys) e atribua questões a eles utilizando o painel admin
4. **Disparo de E-mails**:
    - Envie convites para respondentes participarem das pesquisas. Apenas usuários superadmin podem realizar esse disparo.
5. **Coleta de Respostas:**
    - Respondentes acessam o link do formulário, respondem as questões e suas respostas são armazenadas no sistema.
6. **Visualização de Respostas:**
    - No painel admin, visualize todas as respostas associdas a cada formulário e respondente.

## 🛠️ Endpoints da API
**🔒 Autenticação**
- POST /api-token-auth/
    - Descrição: Gera um token de autenticação para o usuário.
- Corpo da Requisição:
```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```
- Resposta:
```json
{
  "token": "seu_token_aqui"
}
```
### 🛠️ 🗃️ Endpoints Protegidos (Requer Token)
- GET /api/v1/
    - Descrição: Lista todos os endpoints disponíveis da aplicação Surveys.
    - Cabeçalho: Authorization: Token seu_token_aqui

- GET /api/v1/surveys
    - Descrição: Retorna a lista de todos os formulários criados.
    - Cabeçalho: Authorization: Token seu_token_aqui

- GET /api/v1/responses
    - Descrição: Retorna a lista de todas as respostas, incluindo quem respondeu, qual formulário foi respondido e a data de envio.
    - Cabeçalho: Authorization: Token seu_token_aqui

- GET /api/v1/respondents
    - Descrição: Retorna os respondentes cadastrados no sistema.
    - Cabeçalho: Authorization: Token seu_token_aqui

- GET /api/v1/answers
    - Descrição: Retorna as respostas das perguntas, mostrando a questão e a resposta correspondente.
    - Cabeçalho: Authorization: Token seu_token_aqui

- GET /api/v1/questions
    - Descrição: Retorna o ID da questão, o texto da questão e o tipo da questão (text, yes_no, rating).
    - Cabeçalho: Authorization: Token seu_token_aqui

## 📧 Disparo de E-mails
O sistema permite o envio de convites para participação nas pesquisas através do painel admin do Django. Apenas usuários com privilégios de superadmin podem disparar e-mails.

- Passo a Passo:
    - Acesse o painel admin (/admin/).
    - Navegue até a parte inicial do Admin.
    - Selecione o Usuario e o Formulário desejado

- Observação: Lembre-se de criar o .env com as configurações do SMTP

## 📧 📝 Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.