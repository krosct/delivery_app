# TODO - Documentação Faltante de Requisitos e Features

Abaixo está o levantamento das funcionalidades específicas que não foram devidamente documentadas nos arquivos `.feature` dentro dos respectivos diretórios de domínio. Os responsáveis devem criar/atualizar os documentos baseando-se nas orientações do `features/baseline.md`.

## 1. Restaurantes (Responsável: Gabriel)
- [ ] Mover/Consolidar as features de `features/cadastro_restaurante.feature` para dentro do diretório `features/restaurante/`.
- [ ] Documentar o fluxo de **Remoção e Atualização** de cadastro (atualmente o foco está apenas na inserção e validação de acesso).
- [ ] O arquivo `recebimento_notificacao_restaurante.feature` existe, mas validar se contempla corretamente a regra de "notificação de novos pedidos".

## 2. Entregadores (Responsável: Matheus)
- [ ] Criar diretório `features/entregadores/`.
- [ ] Mover/Renomear `features/deliverers.feature` para `features/entregadores/cadastro_manutencao.feature`.
- [ ] Criar feature: **Avaliação de entregas** (`features/entregadores/avaliacao_entregas.feature`).
- [ ] Criar feature: **Notificação de novas entregas** (`features/entregadores/notificacao_entregas.feature`).

## 3. Fazer Pedidos (Responsável: Matheus Braga)
- [ ] Criar diretório `features/pedidos/`.
- [ ] Mover e aprofundar a feature `features/carrinho_compras.feature` para dentro de `features/pedidos/`.
- [ ] Criar feature: **Cancelamento de pedidos** (`features/pedidos/cancelamento_pedidos.feature`).
- [ ] Criar feature: **Cálculo de tempo estimado de entrega** (`features/pedidos/estimativa_entrega.feature`).
- [ ] Criar feature: **Notificação de confirmação do pedido** (`features/pedidos/notificacao_confirmacao.feature`).
- [ ] Criar feature: **Histórico de pedidos** (`features/pedidos/historico_pedidos.feature`).

## 4. Cardápio (Responsável: Pedro)
- [ ] Criar diretório `features/cardapio/`.
- [ ] Mover a feature base de `features/cardapio.feature` para o diretório e dividi-la/ampliá-la.
- [ ] Garantir documentação para: **Cadastro e manutenção de itens**.
- [ ] Criar feature: **Criação de categorias**.
- [ ] Criar feature: **Geração de link de compartilhamento de página personalizada**.

## 5. Pagamento (Responsável: Karol)
- [ ] Criar diretório `features/pagamento/`.
- [ ] Mover/Aprimorar `features/Pagamento.feature` para dentro da pasta com nome padronizado.
- [ ] Criar feature: **Cadastro e manutenção de métodos de pagamento**.
- [ ] Criar feature: **Cadastro e manutenção de promoções**.
- [ ] Criar feature: **Disparo de e-mails de comprovante**.

## 6. Clientes (Responsável: João e Rômulo)
- [ ] Criar diretório `features/clientes/`.
- [ ] Mover `features/clientes.feature` para o diretório.
- [ ] Documentar corretamente: **Cadastro e manutenção** de contas.
- [ ] Criar feature: **Histórico de pedidos do cliente**.
- [ ] Criar feature: **Estatísticas mensais (quantidade total, no mês e preço médio)**.
- [ ] Criar feature: **Recuperação de conta/senha**.