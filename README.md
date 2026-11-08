# 📄 Resume.AI — Sistema de Resumo de PDFs com Histórico e Autenticação

O **Resume.AI** é um sistema web desenvolvido em **Django** com foco em produtividade, permitindo que usuários façam upload de arquivos PDF e recebam um resumo automático gerado por IA.  
Além disso, o sistema conta com funcionalidades de autenticação completa, histórico de arquivos resumidos e gerenciamento de perfil.

---

## 📂 Como Rodar Localmente o Projeto

No ambiente Linux:

```console
git clone https://github.com/Paola403/Resume.AI.git
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
cd resume_ai/
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py runserver
```

No ambiente Windows:

```console
git clone https://github.com/Paola403/Resume.AI.git
pip install virtualenv venv
cd venv
cd scripts
activate.bat
cd ..
cd ..
pip install -r requirements.txt
cd resume_ai/
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py runserver

```
---

## ⚙️ Colocando a chave da API

- Renomeie o .env.example para apenas **.env**
- Coloque a **chave** da API do Google AI (Gemini)

---

## 🚀 Tecnologias Utilizadas

- **Python 3**
- **Django**
- **HTML + CSS + JavaScript**
- **Gemini AI (para resumo)**
- **SQLite**
- **dotenv**
- **pypdf**

---

## 🧩 Funcionalidades Principais

### 🔐 Autenticação
- Cadastro de usuário  
- Login  
- Logout  
- Alterar dados do perfil  
- Alterar senha
- Deletar conta


### 📄 Resumo de PDF
- Upload de arquivos PDF  
- Extração automática do texto  
- Envio para IA gerar resumo  
- Exibição na interface  
- Salvamento automático no histórico  

---

## 🧪 Testes Automatizados

O projeto inclui testes cobrindo:

- Registro  
- Login e logout  
- Alteração de dados  
- Alteração de senha  
---


## 📌 Diferenciais

- Histórico completo de arquivos gerados

- Interface simples e intuitiva

- Integração com inteligência artificial

- Código organizado e fácil de manter

---

## 🔧 Melhorias Futuras

- Melhorar layout final das telas
- Tema escuro
- Exportar resumo para PDF
- Gestão de favoritos
- Resumos de Textos e Imagens
- Código de verificação para _esqueci senha_

---

## 🏗️ Status do Projeto
_Este projeto ainda está em desenvolvimento e NÃO está 100% finalizado._


