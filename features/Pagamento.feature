# "Cadastro e manutenção de métodos de pagamento (inserir, remover, atualizar);
# Cadastro e manutenção de promoções (inserir, remover, atualizar);
# Disparo de emails para usuários com comprovante de pedido;"

Feature: : Aplicar cupom de desconto válido
Dado que existe um pedido com ID “PEDIDO123” e valor total de “100,00”
E o pedido está com status “aguardando pagamento”
E existe um cupom “DESCE20” que oferece “20%” de desconto dentro do prazo de validade
Quando o cliente insere o cupom “DESCE20” na tela de pagamento
Então o valor final da compra é atualizado para “80,00
Então o cliente recebe uma mensagem de confirmação do desconto aplicado
