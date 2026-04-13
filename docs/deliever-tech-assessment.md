# 🚚 Feature Entregadores - Tech Assessment

| Jira Epic | Delivery - Gestão de Entregadores |
| --- | --- |
| Author | Matheus Borges |
| Version | 1.0 |

---

# Objectives

## Problem Statement

Atualmente, o sistema de delivery não possui uma forma estruturada de gerenciar entregadores e vinculá-los aos pedidos. Isso dificulta a distribuição eficiente das entregas, o controle de disponibilidade e a rastreabilidade do processo.

---

## Goals

- Permitir o cadastro e gerenciamento de entregadores  
- Permitir a atribuição de entregadores a pedidos  
- Suportar atribuição automática baseada em regras simples (disponibilidade e região)  
- Garantir rastreabilidade do fluxo de entrega  

---

## Success Criteria

- Um pedido pode ser atribuído corretamente a um entregador disponível  
- O status do pedido e do entregador são atualizados corretamente  
- O sistema consegue reatribuir pedidos em caso de falha  
- Cenários BDD são executáveis e passam com sucesso  

---

# Requirements

## Functional Requirements

- O sistema deve permitir cadastrar entregadores  
- O sistema deve permitir atualizar status do entregador (disponível, ocupado, offline)  
- O sistema deve listar entregadores com filtros  
- O sistema deve permitir atribuir entregador a um pedido  
- O sistema deve sugerir automaticamente um entregador disponível  
- O sistema deve reatribuir pedidos em caso de recusa ou timeout  

---

## Non-Functional Requirements

- **Performance:**
  - Resposta de atribuição < 500ms  
- **Usabilidade:**
  - Interface simples para gestão de entregadores  
- **Consistência:**
  - Atualizações de status devem ser atômicas  
- **Escalabilidade:**
  - Estrutura preparada para futura evolução (event-driven)  

---

## Dependencies

- Banco de dados PostgreSQL  
- Serviço de pedidos (Order)  
- Docker para execução local  

---

# Technical Approach

## Architecture / System Design

Arquitetura baseada em **Hexagonal + Diplomat**, com separação clara entre domínio, aplicação e infraestrutura.

Fluxo principal:

```text
Request HTTP → Controller → Service → Domain → Repository → Database
Key Components
Endpoint (API)
Criar endpoint para atribuição de entregador
POST /orders/{id}/assign
Criar endpoint para gestão de entregadores
POST /deliverers
PATCH /deliverers/{id}/status
GET /deliverers
Frontend
Tela de listagem de entregadores
Filtros por status e região
Tela de atribuição de pedido
Seleção manual de entregador
Feedback visual de status (disponível / ocupado)
Backend
Deliverer Service
Criar entregador
Atualizar status
Buscar por região e disponibilidade
Order Service
Atribuir entregador ao pedido
Atualizar status do pedido
Exemplo de endpoint
POST /orders/{id}/assign

Response:
{
  "order_id": "123",
  "status": "IN_DELIVERY",
  "deliverer_id": "456"
}
Database
Tabela: deliverers
id (UUID)
name
phone
region
vehicle_type
status
Tabela: orders
id (UUID)
status
region
assigned_deliverer_id
Algorithms or Logic
Regra de atribuição
Buscar entregadores disponíveis
Filtrar por região
Selecionar primeiro disponível (simples para projeto acadêmico)
Atualizar:
pedido → IN_DELIVERY
entregador → OCCUPIED
Regra de reatribuição
Detectar timeout ou recusa
Remover entregador atual
Retornar pedido para fila
Executar nova atribuição
Libraries/Tools
Django → API e backend
PostgreSQL → persistência
pytest / pytest-bdd → testes
Docker → containerização
Risks & Tradeoffs
Area	Risk / Tradeoff	Mitigation Strategy
Performance	Crescimento de entregadores pode impactar busca	Uso de filtros simples e indexação
Security	Manipulação de status indevida	Validação no backend
Complexity	Overengineering da arquitetura	Manter regras simples
Technical Debt	Lógica simples de seleção	Evoluir futuramente
Monitoring
Errors
Falha ao atribuir entregador
Pedido sem entregador disponível
Monitoring & Observability
Métricas:
tempo de atribuição
número de pedidos pendentes
Logs:
atribuições realizadas
falhas de reatribuição
Rollout Plan
Feature inicialmente sem feature flag (escopo acadêmico)
Deploy local via Docker
Testes automatizados antes de validação
Milestones
Cadastro de entregadores
Listagem e filtros
Atribuição manual
Atribuição automática
Reatribuição
Open Questions
Como definir prioridade entre entregadores no futuro?
Deve existir limite de pedidos simultâneos por entregador?
Como evoluir para geolocalização real?
Review Status
 Revisão por colega
 Validação com monitor
🔥 Observação final
Esse design prioriza:
Simplicidade de implementação
Clareza de domínio
Aderência a BDD
Facilidade de evolução futura