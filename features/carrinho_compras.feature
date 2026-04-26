Funcionalidade: Gerenciamento do Carrinho
    Como um cliente da plataforma de delivery
    Quero poder adicionar, remover e visualizar itens no meu carrinho de compras
    Para que eu possa revisar meu pedido antes de finalizar a compra

Cenário de Serviço: Adição bem-sucedida de item com customizações ao carrinho
    Given que o usuário "João Silva" está autenticado no sistema
    And o carrinho do usuário "João Silva" está aberto para o restaurante "McDonalds"
    And o item "X-Burguer" do restaurante "McDonalds" está no carrinho
    And o adicional "Bacon Extra" é adicionado ao carrinho
    When o serviço recebe uma requisição para adicionar ao carrinho:
    Then o carrinho do usuário "João Silva" passa a conter o item "X-Burguer" com o adicional "Bacon Extra"
    And o subtotal do carrinho passa a ser "R$ 32,00"
