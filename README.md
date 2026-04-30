# Delivery App - Sistema de Gestão e Pedidos

## Visão Geral Técnica e de Negócios

O **Delivery App** é uma plataforma abrangente projetada para conectar clientes a restaurantes, facilitando o processo de pedidos, acompanhamento de entregas e gestão operacional para os lojistas e entregadores. O sistema atua como um intermediário eficiente, garantindo uma experiência fluida de ponta a ponta.

### Escopo Geral
O ecossistema é dividido em seis domínios principais:
1. **Restaurantes:** Gestão do estabelecimento e recebimento de pedidos.
2. **Entregadores:** Gestão de rotas, avaliação e status de entrega.
3. **Pedidos:** Core da aplicação, controlando desde o carrinho de compras até o histórico de pedidos.
4. **Cardápio:** Vitrine de produtos, categorias e links personalizados.
5. **Pagamento:** Gestão de métodos, promoções e emissão de comprovantes.
6. **Clientes:** Perfil do usuário, estatísticas de consumo e recuperação de acesso.

## Tabela de Responsabilidade por Domínios

| Domínio | Responsável(is) | Papel / Foco Principal |
|---------|-----------------|------------------------|
| Restaurantes | Gabriel | Cadastro, manutenção e gestão de notificações. |
| Entregadores | Matheus | Roteamento, avaliações e alertas de entrega. |
| Pedidos | Matheus Braga | Carrinho, status, estimativas e cancelamento. |
| Cardápio | Pedro | Gestão de itens, categorias e vitrine web. |
| Pagamento | Karol | Gateways, métodos, promoções e e-mails (comprovantes). |
| Clientes | João e Rômulo | Gestão de perfis, histórico e analytics do cliente. |

## Arquitetura Tecnológica

**Stack Principal (Atual):**
- **Frontend:** ReactJS (com TypeScript e Vite)
- **Backend:** NodeJS (Express/NestJS) - *Nota: Transição da estrutura legada em Python/Django*
- **Bancos de Dados:** MySQL (Relacional) e Redis (Cache e Filas)

**Tecnologias Adicionais Sugeridas (Cruciais):**
- **RabbitMQ ou Apache Kafka:** Para mensageria assíncrona entre os microserviços (ex: notificação de pedidos e pagamentos).
- **Socket.io / WebSockets:** Essencial para rastreamento de entregadores em tempo real e notificações live para restaurantes.
- **Docker & Kubernetes:** Para orquestração escalável.
- **Elasticsearch:** Para otimizar a busca de restaurantes e pratos de forma rápida e inteligente.
- **AWS S3 / MinIO:** Para armazenamento de imagens de cardápios e avatares.

## Estrutura do Projeto (Atual e Futura)

Baseado nas melhores práticas de Engenharia de Software, TDD e BDD:

```text
/delivery_app
├── app/frontend/          # Aplicação SPA em ReactJS
├── service/backend/       # APIs em NodeJS (Organizado por domínios/DDD)
├── docs/                  # Documentação de arquitetura (ADRs, Diagramas)
├── features/              # Especificações BDD (Arquivos .feature por domínio)
├── docker-compose.yml     # Orquestração local
└── README.md              # Este documento central
```

## Como Executar Localmente via Docker

1. **Pré-requisitos:** Certifique-se de ter o Docker e o Docker Compose instalados.
2. **Construir e Iniciar os Contêineres:**
   ```bash
   docker-compose up --build -d
   ```
3. **Verificar os Serviços:**
   - Frontend (React): `http://localhost:5173`
   - Backend (NodeJS): `http://localhost:3000`
   - Banco de Dados (MySQL): Porta `3306`
   - Cache (Redis): Porta `6379`
4. **Parar a Aplicação:**
   ```bash
   docker-compose down
   ```

## Execução da Suíte de Testes (BDD)

Os testes são orientados a comportamento (BDD) baseados nos cenários `.feature`.
No backend (assumindo Jest/Cucumber-js para NodeJS):
```bash
# Executa a suíte completa de testes
docker-compose exec backend npm run test:e2e

# Executa testes de um domínio específico
docker-compose exec backend npm run test:e2e -- --tags "@restaurante"
```

No frontend (assumindo Cypress):
```bash
docker-compose exec frontend npm run cypress:run
```

## Resultados Esperados por Domínio (Fim do Projeto)

- **Restaurantes:** Sistema capaz de cadastrar, remover e atualizar perfis; painel em tempo real para recebimento de notificações de novos pedidos.
- **Entregadores:** Gestão de frota eficiente, com métricas de avaliação e sistema robusto de dispatch (notificação de novas entregas).
- **Pedidos:** Fluxo de carrinho livre de atritos, precisão no cálculo de ETA (Tempo Estimado de Entrega), e funcionalidades seguras de cancelamento e visualização de histórico.
- **Cardápio:** Gestor de cardápios flexível com suporte a categorias dinâmicas e capacidade de gerar links públicos para divulgação via redes sociais.
- **Pagamento:** Integração com múltiplos meios (cartão, Pix), motor de promoções/cupons operante e sistema confiável de envio de e-mails transacionais (comprovantes).
- **Clientes:** Dashboard self-service para clientes gerenciarem seus dados, recuperarem credenciais e visualizarem estatísticas mensais de gastos e consumo.