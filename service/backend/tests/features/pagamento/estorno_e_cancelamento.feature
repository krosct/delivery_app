Feature: Processamento de estornos - BACKEND

  Cenário 1: Processar estorno total via API
    Given o pedido "PEDIDO123" está com status "PAGO"
    And o valor pago foi "100,00"
     And o saldo do cliente "cli_123" é "0,00"
    When eu envio uma requisição POST para "/api/pagamento/estornar/PEDIDO123"
    Then o status deve ser 200 OK
    And o pedido deve ter status "CANCELADO"
    And o saldo do cliente deve ser "100,00"

  Cenário 2: Impedir estorno após aceite do restaurante
    Given o pedido "PEDIDO123" está com status "PREPARANDO"
    When eu envio uma requisição POST para "/api/pagamento/estornar/PEDIDO123"
    Then o status deve ser "400 BAD REQUEST"
    And a mensagem deve ser "Pedido não pode ser cancelado após aceite do restaurante"
    And o status do pedido deve permanecer "PREPARANDO"
