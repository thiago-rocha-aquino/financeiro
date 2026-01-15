# FinanceApp - Sistema de Controle Financeiro

Sistema completo de controle financeiro pessoal desenvolvido com **Clean Architecture** no backend e **Next.js** no frontend.

## Tecnologias

### Backend
- **FastAPI** - Framework web moderno e de alta performance

### Frontend
- **Next.js ** - Framework React com App Router

## Arquitetura

### Backend - Clean Architecture

```
backend/
├── src/
│   ├── domain/           # Regras de negócio
│   │   ├── entities/     # Entidades de domínio
│   │   ├── repositories/ # Interfaces de repositório
│   │   └── services/     # Interfaces de serviços
│   ├── application/      # Casos de uso
│   │   ├── dtos/         # Data Transfer Objects
│   │   └── use_cases/    # Casos de uso da aplicação
│   ├── infrastructure/   # Implementações
│   │   ├── config/       # Configurações
│   │   ├── database/     # ORM e repositórios
│   │   └── security/     # Autenticação
│   └── presentation/     # API REST
│       └── api/          # Routers FastAPI
└── tests/
```

### Frontend - Feature-based

```
frontend/
├── src/
│   ├── app/              # App Router (páginas)
│   │   ├── (app)/        # Páginas autenticadas
│   │   └── auth/         # Autenticação
│   ├── components/       # Componentes React
│   │   ├── ui/           # Componentes base (ShadCN)
│   │   ├── layout/       # Layout da aplicação
│   │   ├── forms/        # Formulários
│   │   └── charts/       # Gráficos
│   ├── hooks/            # Custom hooks
│   ├── lib/              # Utilitários
│   ├── services/         # Chamadas API
│   └── types/            # Tipos TypeScript
```

## Funcionalidades

- **Autenticação** - Cadastro, login com JWT
- **Dashboard** - Visão geral das finanças
- **Transações** - CRUD de receitas e despesas
- **Categorias** - Organização por categorias
- **Orçamentos** - Controle de gastos mensais por categoria
- **Gráficos** - Visualização de dados

## Como Executar

### Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependências
pip install -e .

# Copiar variáveis de ambiente
cp .env.example .env

# Executar
uvicorn src.main:app --reload
```

API disponível em: http://localhost:8000
Documentação: http://localhost:8000/docs

### Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Copiar variáveis de ambiente
cp .env.local.example .env.local

# Executar
npm run dev
```

Aplicação disponível em: http://localhost:3000

### Docker Compose

```bash
# Executar tudo
docker-compose up -d

# Parar
docker-compose down
```

## API Endpoints

### Autenticação
- `POST /api/v1/auth/register` - Cadastro
- `POST /api/v1/auth/login` - Login

### Usuários
- `GET /api/v1/users/me` - Dados do usuário
- `PATCH /api/v1/users/me` - Atualizar usuário

### Transações
- `GET /api/v1/transactions` - Listar transações
- `POST /api/v1/transactions` - Criar transação
- `PATCH /api/v1/transactions/{id}` - Atualizar transação
- `DELETE /api/v1/transactions/{id}` - Deletar transação
- `GET /api/v1/transactions/summary` - Resumo financeiro

### Categorias
- `GET /api/v1/categories` - Listar categorias
- `POST /api/v1/categories` - Criar categoria
- `PATCH /api/v1/categories/{id}` - Atualizar categoria
- `DELETE /api/v1/categories/{id}` - Deletar categoria

### Orçamentos
- `GET /api/v1/budgets` - Listar orçamentos
- `POST /api/v1/budgets` - Criar orçamento
- `PATCH /api/v1/budgets/{id}` - Atualizar orçamento
- `DELETE /api/v1/budgets/{id}` - Deletar orçamento

## Padrões de Código

### Backend
- **Clean Architecture** - Separação de responsabilidades

### Frontend
- **Component Composition** - Componentes reutilizáveis
- **Custom Hooks** - Lógica compartilhada


