# 📄 Resume.AI — Sistema de Resumo de PDFs com Histórico e Autenticação

O **Resume.AI** é um sistema web desenvolvido em **Django** com foco em produtividade, permitindo que usuários façam upload de arquivos PDF e recebam um resumo automático gerado por Inteligência Artificial.

Além disso, o sistema conta com funcionalidades de autenticação completa, histórico de arquivos resumidos e gerenciamento de perfil.

---

## 📂 Como Rodar Localmente o Projeto

### 🐧 Ambiente Linux

```bash
git clone https://github.com/Paola403/Resume.AI.git
cd Resume.AI

virtualenv -p python3 venv
source venv/bin/activate

pip install -r requirements.txt

cd resume_ai/

python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py runserver
```

### 🪟 Ambiente Windows

```bash
git clone https://github.com/Paola403/Resume.AI.git
cd Resume.AI

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

cd resume_ai/

python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py runserver
```

Após iniciar o servidor, acesse:

```text
http://127.0.0.1:8000/
```

---

## 🐳 Executando com Docker e Docker Compose

O projeto também pode ser executado utilizando **Docker** e **Docker Compose**, permitindo configurar o ambiente da aplicação de maneira padronizada, sem precisar instalar manualmente as dependências do Python na máquina.

### ⚙️ Pré-requisitos

Antes de iniciar, é necessário ter instalado:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — Windows e macOS.
- Docker Engine e Docker Compose — Linux.

No Windows, basta abrir o Docker Desktop e aguardar até que o Docker esteja em execução.

Para verificar se a instalação está funcionando, execute:

```bash
docker --version
docker compose version
```

### 📁 Arquivos de configuração

Na raiz do projeto, foram adicionados os seguintes arquivos:

```text
Resume.AI/
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
│
└── resume_ai/
    ├── manage.py
    ├── .env
    └── ...
```

**Responsabilidade de cada arquivo:**

- **Dockerfile:** define como a imagem da aplicação será construída, incluindo a versão do Python, instalação das dependências e inicialização do Django.
- **docker-compose.yml:** configura e executa os serviços da aplicação, portas, variáveis de ambiente e volumes.
- **.dockerignore:** determina quais arquivos e pastas não devem ser enviados durante a construção da imagem.
- **requirements.txt:** contém as bibliotecas Python necessárias para executar o projeto.

### 🔑 Configuração das variáveis de ambiente

Antes de iniciar a aplicação, configure o arquivo `.env`.

Caso exista apenas o arquivo `.env.example`, faça uma cópia e renomeie para `.env`.

Exemplo:

```env
DJANGO_SECRET_KEY=sua_chave_secreta_django
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

GEMINI_API_KEY=sua_chave_api_gemini
```

A variável `DJANGO_SECRET_KEY` deve conter uma chave secreta gerada para o Django. Não utilize o texto de exemplo como valor definitivo.

A variável `GEMINI_API_KEY` deve conter a chave de acesso à API do Google Gemini.

**Importante:** o arquivo `.env` contém informações privadas e não deve ser enviado ao GitHub.

### 🚀 Construindo e iniciando a aplicação

Com o Docker Desktop em execução, abra o terminal na pasta raiz do projeto, onde está localizado o arquivo `docker-compose.yml`.

**1. Construir a imagem e iniciar o container:**

```bash
docker compose up --build
```

Esse comando realiza as seguintes etapas:

- Lê as configurações do Docker Compose.
- Constrói a imagem utilizando o Dockerfile.
- Instala as dependências definidas no `requirements.txt`.
- Cria e inicia o container da aplicação.
- Executa as migrações do banco de dados.
- Inicializa o servidor Django.

**2. Acessar a aplicação:**

Após a inicialização, acesse:

```text
http://localhost:8000/
```

**3. Executar em segundo plano (opcional):**

Caso queira iniciar a aplicação sem manter o terminal ocupado:

```bash
docker compose up -d --build
```

### 🔍 Comandos úteis do Docker

| Comando | Descrição |
|---|---|
| `docker compose up` | Inicia os serviços. |
| `docker compose up --build` | Reconstrói a imagem e inicia os serviços. |
| `docker compose up -d` | Inicia os serviços em segundo plano. |
| `docker compose ps` | Lista os containers do projeto. |
| `docker compose logs -f` | Exibe os logs da aplicação. |
| `docker compose stop` | Interrompe os containers. |
| `docker compose start` | Inicia containers que foram interrompidos. |
| `docker compose down` | Para e remove os containers e a rede do projeto. |

**Observação sobre os dados:** o projeto utiliza volumes Docker para persistir os dados do SQLite e os arquivos de mídia. Assim, os dados permanecem armazenados mesmo quando os containers são removidos com `docker compose down`.

Para remover também os volumes e os dados persistidos, utilize:

```bash
docker compose down -v
```

**Atenção:** esse comando apaga os dados armazenados nos volumes do projeto.

---

## ⚙️ Colocando a chave da API

- Renomeie o arquivo `.env.example` para `.env`.
- Insira a chave da API do Google AI (Gemini).
- Configure também as variáveis necessárias para o funcionamento do Django.

---

## 🚀 Tecnologias Utilizadas

- **Python 3**
- **Django**
- **HTML + CSS + JavaScript**
- **Gemini AI** — geração automática de resumos.
- **SQLite** — banco de dados.
- **python-dotenv** — gerenciamento de variáveis de ambiente.
- **pypdf** — extração de texto de arquivos PDF.
- **Docker** — conteinerização da aplicação.
- **Docker Compose** — gerenciamento e execução dos containers.

---

## 🧩 Funcionalidades Principais

### 🔐 Autenticação

- Cadastro de usuário.
- Login.
- Logout.
- Alteração de dados do perfil.
- Alteração de senha.
- Exclusão de conta.

### 📄 Resumo de PDF

- Upload de arquivos PDF.
- Extração automática do texto.
- Envio do conteúdo para a IA gerar o resumo.
- Exibição do resumo na interface.
- Salvamento automático no histórico.

---

## 🧪 Testes Automatizados

O projeto inclui testes automatizados cobrindo:

- Registro de usuários.
- Login e logout.
- Alteração de dados.
- Alteração de senha.

Para executar os testes localmente:

```bash
python manage.py test
```

Para executar os testes dentro do container:

```bash
docker compose exec resume-ai python manage.py test
```

---

## 📌 Diferenciais

- Histórico completo de arquivos resumidos.
- Interface simples e intuitiva.
- Integração com Inteligência Artificial.
- Código organizado e fácil de manter.
- Ambiente de execução padronizado com Docker.
- Persistência de dados por meio de volumes Docker.

---

## 🔧 Melhorias Futuras

- Melhorar o layout final das telas.
- Implementar tema escuro.
- Exportar resumos para PDF.
- Implementar gestão de favoritos.
- Permitir resumos de textos e imagens.
- Implementar código de verificação para recuperação de senha.

---

## 🏗️ Status do Projeto

*Este projeto ainda está em desenvolvimento e não está 100% finalizado.*