# 😋 Yummicious 😋

Projeto de delivery construído como um monólito modular com backend em FastAPI, persistência MySQL via SQLAlchemy e frontend em React + Vite + TypeScript.

O objetivo desta base é entregar um MVP funcional para o fluxo de entregas, com uma arquitetura fácil de entender, testar e evoluir por feature.

## Visão geral

### Objetivo do MVP

Resolver o ciclo operacional de delivery:

cliente faz o pedido, o restaurante prepara, o entregador assume a entrega e o pedido é finalizado com rastreabilidade mínima do fluxo.

### Escopo atual

- Deliverer backend concluído
- Deliverer frontend concluído e modularizado
- BDD do Deliverer implementado
- Testes de serviço, integração, frontend e build validados
- Outros módulos ainda em evolução, com níveis diferentes de maturidade

### Tecnologias

- FastAPI
- SQLAlchemy
- Alembic
- MySQL
- React
- Vite
- TypeScript
- Jest
- Testing Library
- pytest
- pytest-bdd

### Arquitetura atual

- Backend organizado por módulos de domínio em `backend/modulos/`
- Frontend organizado por feature em `frontend/src/features/`
- Camada compartilhada em `frontend/src/shared/`
- BDD como documentação executável do comportamento

### Motivos da simplificação

- Evitar microsserviços antes da hora
- Manter o fluxo de negócio dentro de um único repositório
- Facilitar testes, leitura do código e onboarding
- Permitir evolução por feature sem quebrar o que já funciona

## Estrutura do projeto

- `backend/`: API FastAPI, domínio, serviços, repositórios e migrações
- `frontend/`: aplicação React/Vite com a feature Deliverer isolada
- `bdd/`: especificações BDD do backend e do frontend
- `database/`: scripts e esquemas do banco
- `tests/`: cenários BDD e testes de apoio
- `docker-compose.yml`: orquestra a base MySQL e os containers de aplicação

## Como rodar o projeto completo

A forma mais previsível de rodar tudo hoje é iniciar o banco com Docker e subir backend e frontend em processos separados.

### Comandos via Makefile

Os alvos principais são:

```bash
make build-db      # sobe só o banco
make build-backend # sobe só o backend
make build-frontend # sobe só o frontend
make up            # sobe o stack completo
make down          # derruba os containers
make logs          # acompanha os logs
make test          # roda backend + frontend
```

### 1. Subir o banco de dados

```bash
docker compose up db -d
```

O backend usa as variáveis abaixo, com defaults definidos em `backend/core/config.py`:

- `DB_HOST` = `db`
- `DB_PORT` = `3306`
- `DB_USER` = `delivery_user`
- `DB_PASSWORD` = `delivery_pass`
- `DB_NAME` = `yummicious_db`
- `SECRET_KEY` = `super-secret-key-change-it-in-production`
- `TZ` = `America/Sao_Paulo`

### 2. Subir o backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API principal:

- `http://localhost:8000`
- documentação automática em `http://localhost:8000/docs`

### 3. Subir o frontend

```bash
cd frontend
npm install
npm run dev
```

O Vite roda em `http://localhost:4173` com a configuração atual do projeto.

### 4. Rodar o fluxo completo

Com os três serviços ativos, o fluxo esperado é:

- banco MySQL em execução
- API FastAPI respondendo em `:8000`
- frontend React disponível em `:4173`

## Pontos de conexão por feature

### Deliverer

- Backend: `backend/modulos/delivery/http/api.py`
- Domínio: `backend/modulos/delivery/domain/`
- Serviço: `backend/modulos/delivery/application/services/deliverers_service.py`
- Persistência: `backend/modulos/delivery/infrastructure/`
- Frontend: `frontend/src/features/deliverer/`
- Testes: `backend/tests/test_deliverers_service.py`, `backend/tests/test_deliverers_integration.py`, `backend/tests/test_bdd_deliverer.py`, `frontend/src/features/deliverer/__tests__/`

### Cardápio

- Backend: `backend/modulos/cardapio/rotas.py`
- Controle: `backend/modulos/cardapio/controle.py`
- API montada em `backend/main.py` com prefixo `/api/v1`

### Cliente

- Backend: `backend/modulos/cliente/rotas.py`
- Serviço: `backend/modulos/cliente/cliente_service.py`
- Repositório: `backend/modulos/cliente/cliente_repository.py`
- API montada em `backend/main.py` com prefixo `/api/v1`

### Restaurante

- Backend: `backend/modulos/restaurante/rotas.py`
- Controle: `backend/modulos/restaurante/controle.py`
- API montada em `backend/main.py` com prefixo `/api/v1`

### Pagamento

- Backend: `backend/modulos/pagamento/rotas.py`
- Controle: `backend/modulos/pagamento/controle.py`
- Estado atual: módulo disponível no código, mas ainda com integração incompleta no ponto de entrada principal

### Pedido

- Backend: `backend/modulos/pedido/`
- Estado atual: ainda como placeholder

## Como o backend está conectado

O ponto de entrada é `backend/main.py`, que registra os routers modulares e expõe a aplicação FastAPI.

Resumo do encadeamento:

```text
FastAPI app
↓
Routers por módulo
↓
Services / Controls
↓
Repositories / Conexão com banco
↓
MySQL
```

## Como o frontend está organizado

O frontend foi refatorado para feature driven architecture.

Estrutura principal:

```text
frontend/src/
   app/
   features/
      deliverer/
   shared/
```

### Ponto de entrada

- `frontend/src/app/App.tsx`: compõe a aplicação
- `frontend/App.tsx`: wrapper legado para compatibilidade

### Feature Deliverer

Dentro de `frontend/src/features/deliverer/` a feature foi separada em:

- `api/`: chamadas HTTP
- `services/`: regras e utilitários de estado
- `hooks/`: orquestração de dados e comportamento
- `components/`: blocos reutilizáveis de UI
- `pages/`: telas do usuário
- `routes/`: composição das páginas

### Shared

`frontend/src/shared/` concentra componentes e helpers reutilizáveis para evitar duplicação.

## Progresso geral

### Concluído

- Deliverer backend completo
- Persistência SQLAlchemy e migração Alembic
- Endpoints FastAPI do Deliverer
- State machine de entregador e entrega
- Auditoria e rastreio de transições
- BDD do Deliverer
- Testes de serviço e integração do backend
- Frontend Deliverer modularizado
- Hooks, services, components, pages e routes separados
- Testes frontend em jsdom
- Build do frontend validado

### Em evolução

- Cardápio, cliente, restaurante e pagamento ainda seguem em bases menos modernas que o Deliverer
- Pedido ainda está como placeholder
- O frontend possui a feature Deliverer pronta, mas as demais features ainda dependem de evolução

## Como rodar os testes

### Backend e BDD

```bash
cd backend
pytest
```

### Frontend

```bash
npm test -- --runInBand
```

### Build do frontend

```bash
npm run build:frontend
```

## Evidências da feature Deliverer

### Endpoints principais

- `GET /api/deliverers/`
- `POST /api/deliverers/`
- `PATCH /api/deliverers/{deliverer_id}/status/`
- `POST /api/orders/assign/`
- `GET /api/orders/`
- `POST /api/orders/{order_id}/reassign/`
- `POST /api/orders/{order_id}/accept/`
- `PATCH /api/orders/{order_id}/pickup/`
- `PATCH /api/orders/{order_id}/deliver/`

### Cenários BDD e testes

- Cenário de cadastro de entregador em `tests/deliverer.feature`
- Testes unitários em `backend/tests/test_deliverers_service.py`
- Testes de integração em `backend/tests/test_deliverers_integration.py`
- Testes BDD em `backend/tests/test_bdd_deliverer.py`
- Testes frontend do módulo Deliverer em `frontend/src/features/deliverer/__tests__/`

## Como adicionar uma nova feature

1. Crie o módulo backend em `backend/modulos/<feature>/`.
2. Separe domínio, serviços, controles ou rotas e persistência.
3. Exponha os endpoints no `main.py` via router modular.
4. Crie a feature correspondente no frontend dentro de `frontend/src/features/<feature>/`.
5. Coloque componentes compartilhados em `frontend/src/shared/` somente quando houver reaproveitamento real.
6. Escreva testes unitários, integração e BDD para o novo fluxo.

## Boas práticas de colaboração

- Use branches pequenas e focadas por feature.
- Escreva commits descritivos e orientados ao comportamento.
- Documente endpoints, exemplos de uso e testes executados no PR.

## Observações finais

Esta base evoluiu para um monólito modular com uma feature Deliverer bem definida. O README agora reflete a estrutura real do projeto, os pontos de conexão de cada módulo e o estado atual de progresso para apoiar desenvolvimento, manutenção e apresentação técnica.
