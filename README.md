# Mello Finance API

API financeira pessoal desenvolvida com **FastAPI + PostgreSQL + SQLAlchemy**, com arquitetura modular e preparada para futuras integrações com IA, Telegram e automações financeiras.

O objetivo da Mello é centralizar controle financeiro, permitindo cadastro de usuários, contas bancárias, categorias e movimentações financeiras.

---

# 🚀 Tecnologias

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* Uvicorn
* Docker (planejado)
* Swagger/OpenAPI

---

# 🏗️ Arquitetura

A aplicação segue uma separação por responsabilidades:

```
Request HTTP
      |
      ↓
FastAPI Routes
      |
      ↓
Schemas (Pydantic)
      |
      ↓
Services
      |
      ↓
Repositories / Database Functions
      |
      ↓
PostgreSQL
```

## Responsabilidade de cada camada

### API

Recebe requisições HTTP e retorna respostas.

Exemplo:

```
POST /transactions
```

---

### Schemas

Responsáveis pela validação e formato dos dados.

Exemplo:

```json
{
  "description": "Mercado",
  "amount": 150.50,
  "transaction_type": "expense"
}
```

---

### Services

Contém regras de negócio.

Exemplo:

* validar usuário
* validar conta
* processar transação
* controlar fluxo da aplicação

---

### Database Functions / Repositories

Responsáveis pela comunicação com PostgreSQL.

Exemplo:

* INSERT
* UPDATE
* DELETE
* SELECT

---

# 📂 Estrutura

```
app/
│
├── api/
│   ├── routes_users.py
│   ├── routes_accounts.py
│   ├── routes_transactions.py
│   └── routes_categories.py
│
├── schemas/
│   ├── user_schema.py
│   ├── account_schema.py
│   ├── transaction_schema.py
│   └── category_schema.py
│
├── services/
│   ├── user_service.py
│   ├── account_service.py
│   ├── transaction_service.py
│   └── category_service.py
│
├── repositories/
│
├── db/
│   └── conn.py
│
main.py
```

---

# 📌 Funcionalidades V1.5

## Usuários

### Criar usuário

```
POST /users
```

### Listar usuários

```
GET /users
```

### Buscar usuário

```
GET /users/{user_id}
```

### Atualizar usuário

```
PATCH /users/{user_id}
```

### Deletar usuário

```
DELETE /users/{user_id}
```

---

# Contas

Relacionadas aos usuários.

Endpoints:

```
POST /accounts
```

Criar conta bancária.

```
GET /accounts/{account_id}
```

Buscar conta.

```
GET /users/{user_id}/accounts
```

Listar contas do usuário.

```
PATCH /accounts/{account_id}
```

Atualizar conta.

```
DELETE /accounts/{account_id}
```

Excluir conta.

---

# Transações

Responsável por receitas e despesas.

Exemplo:

```json
{
"user_id":1,
"account_id":1,
"category_id":1,
"description":"Mercado",
"amount":150.50,
"transaction_type":"expense"
}
```

Endpoints:

```
POST /transactions
```

Criar movimentação.

```
GET /transactions/{transaction_id}
```

Buscar transação.

```
GET /users/{user_id}/transactions
```

Histórico completo.

```
GET /users/{user_id}/transactions/month
```

Movimentações do mês.

```
GET /accounts/{account_id}/transactions
```

Histórico por conta.

```
PATCH /transactions/{transaction_id}
```

Editar.

```
DELETE /transactions/{transaction_id}
```

Excluir.

---

# Categorias

Exemplos:

* Alimentação
* Transporte
* Moradia
* Lazer
* Outros

Endpoints:

```
GET /categories
```

Listar categorias.

```
POST /categories
```

Criar categoria.

```
PATCH /categories/{category_id}
```

Editar categoria.

```
DELETE /categories/{category_id}
```

Excluir categoria.

---

# Regras de negócio

A API garante:

* Usuário precisa existir antes de criar conta.
* Conta precisa pertencer ao usuário.
* Transação precisa possuir usuário válido.
* Transação precisa possuir conta válida.
* Valores financeiros devem ser positivos.
* Tipos permitidos:

```
expense
income
```

---

# Executando o projeto

Criar ambiente:

```bash
python -m venv .venv
```

Ativar:

Linux:

```bash
source .venv/bin/activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Executar API:

```bash
uvicorn main:app --reload
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

# Banco de Dados

A aplicação utiliza PostgreSQL.

Principais entidades:

```
users
 |
 └── accounts
        |
        └── transactions
                |
                └── categories
```

---

# Próximos passos

## V2

Planejado:

* Integração Telegram
* Assistente financeiro com IA
* Resumos financeiros automáticos
* Alertas inteligentes
* Dashboard financeiro
* Autenticação JWT
* Deploy em cloud

---

# Objetivo do projeto

Transformar a Mello em um assistente financeiro inteligente capaz de registrar, analisar e interpretar dados financeiros utilizando automação e inteligência artificial.
