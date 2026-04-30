# Cronograma do Projeto - Delivery App

Este documento reflete o planejamento estratégico do projeto, estruturado em 5 sprints de 2 semanas cada, visando a entrega iterativa e incremental de valor.

## Visão Geral das Sprints
- **Duração da Sprint:** 2 Semanas
- **Início do Projeto (Sprint 1):** 15/04/2026
- **Sprint Atual (Sprint 2):** Início em 29/04/2026

---

## Sprint 1: Fundação e Elicitação
**Período:** 15/04/2026 a 28/04/2026
**Foco:** Elicitação de requisitos, design de arquitetura, estruturação dos repositórios e confecção inicial de features (BDD).

- [x] Definição de Arquitetura e Stack (NodeJS, React, MySQL, Redis).
- [x] Configuração inicial do repositório (README, estrutura de pastas).
- [x] Elaboração do Baseline BDD (`features/baseline.md`).
- [x] Levantamento de Requisitos - Todos os Domínios.
- [x] Rascunho inicial de Arquivos `.feature`.

**Milestone S1:** Arquitetura definida e documentação base consolidada.

---

## Sprint 2: Core Cadastral e Estrutura de Banco
**Período:** 29/04/2026 a 12/05/2026
**Foco:** Preparação do ambiente Docker, banco de dados, autenticação e CRUDS iniciais.

- **DevOps (Todos):** Configuração final do `docker-compose.yml` e Dockerfiles.
- **Restaurantes (Gabriel):** API e Tela de Cadastro/Manutenção de Restaurantes.
- **Entregadores (Matheus):** API e Tela de Cadastro e manutenção de Entregadores.
- **Clientes (João e Rômulo):** API e Tela de Cadastro e manutenção de Clientes.
- **Cardápio (Pedro):** API de Cadastro/Manutenção de Itens de Cardápio.

**Milestone S2:** Ambiente de desenvolvimento rodando com Docker e fluxos de cadastro finalizados.

---

## Sprint 3: Vitrine, Carrinho e Pedidos Básicos
**Período:** 13/05/2026 a 26/05/2026
**Foco:** Início da interação entre as entidades, com foco na visualização do produto e criação do pedido.

- **Cardápio (Pedro):** Criação de categorias e geração do link de compartilhamento.
- **Pedidos (Matheus Braga):** Implementação do Carrinho de Compras e fluxo inicial de Checkout.
- **Pagamento (Karol):** Cadastro e manutenção de métodos de pagamento.
- **Clientes (João e Rômulo):** Implementação da Recuperação de conta/senha.

**Milestone S3:** Cliente consegue acessar link do restaurante, montar carrinho e iniciar checkout.

---

## Sprint 4: Roteamento, Pagamento e Notificações
**Período:** 27/05/2026 a 09/06/2026
**Foco:** Finalizar a transação financeira, acionar o restaurante e encaminhar para a entrega.

- **Pagamento (Karol):** Processamento de pagamento, disparo de e-mails de comprovante e manutenção de promoções.
- **Pedidos (Matheus Braga):** Cálculo de tempo estimado, notificação de confirmação e histórico.
- **Restaurantes (Gabriel):** Notificação em tempo real de novos pedidos.
- **Entregadores (Matheus):** Notificação de novas entregas e atribuição de rotas.

**Milestone S4:** Fluxo end-to-end do pedido (Cliente paga -> Restaurante aceita -> Entregador é notificado).

---

## Sprint 5: Analytics, Avaliação e Polimento
**Período:** 10/06/2026 a 23/06/2026
**Foco:** Finalização, Edge Cases, Métricas e Estabilização para Lançamento.

- **Entregadores (Matheus):** Sistema de avaliação de entregas.
- **Pedidos (Matheus Braga):** Fluxo seguro de Cancelamento de pedidos.
- **Clientes (João e Rômulo):** Dashboard de estatísticas mensais (quantidade total, no mês e preço médio).
- **Todos:** Refatoração, cobertura final de testes E2E/BDD e correções de bugs.

**Milestone S5:** Projeto pronto, testado e documentado para apresentação final.

---

## Matriz de Integração (Fluxo de Valor)

Para garantir o alinhamento, a integração entre domínios ocorrerá da seguinte forma:

1. O **Restaurante (Gabriel)** cria seu perfil e delega a montagem da vitrine ao **Cardápio (Pedro)**.
2. O **Cliente (João/Rômulo)** acessa o link do cardápio e utiliza as funções de **Pedidos (Matheus Braga)** para montar o carrinho.
3. O checkout aciona as regras de **Pagamento (Karol)**, que confirma a transação e avisa o **Pedido**.
4. O **Pedido** altera seu status, notificando o **Restaurante** para o preparo via WebSockets.
5. Após o preparo, o **Restaurante** despacha o pedido, o qual busca no pool um **Entregador (Matheus)** disponível, notificando-o e estimando o tempo na tela do **Cliente**.