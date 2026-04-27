# "Cadastro e manutenção de métodos de pagamento (inserir, remover, atualizar);
# Cadastro e manutenção de promoções (inserir, remover, atualizar);
# Disparo de emails para usuários com comprovante de pedido;"
# Ajuste questão 8

Feature: : Aplicar cupom de desconto válido
Dado que existe um pedido com ID “PEDIDO123” e valor total de “100,00”
E o pedido está com status “aguardando pagamento”
E existe um cupom “DESCE20” que oferece “20%” de desconto dentro do prazo de validade
Quando o cliente insere o cupom “DESCE20” na tela de pagamento
Então o valor final da compra é atualizado para “80,00
Então o cliente recebe uma mensagem de confirmação do desconto aplicado

Feature: : Aplicar cupom de desconto válido
Dado que existe um pedido com ID “PEDIDO124” e valor total de “100,00”
E o pedido está com status “aguardando pagamento”
E existe um cupom “DESCE20” que oferece “20%” de desconto fora do prazo de validade
Quando o cliente insere o cupom “DESCE20” na tela de pagamento
Então o cliente recebe uma mensagem de erro indicando que o cupom é inválido

Feature: Realizar estorno de saldo ao cancelar pedido
Dado que existe um pedido com ID “PEDIDO123” e valor total de “100,00”
E o pedido está com status “pago”
Quando o cliente solicita cancelamento do pedido antes do restaurante aceitar
Então o status do pedido deve ser atualizado para “Cancelado”
E o valor “100,00” do pedido deve estar disponível no saldo do cliente no sistema
