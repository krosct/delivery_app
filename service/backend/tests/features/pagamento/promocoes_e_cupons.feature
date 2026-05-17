Feature: Gerenciamento de promoções - BACKEND

  Cenário 1: Validar cupom de desconto via API
    Given existe um cupom "DESCE20" com:
      | campo         | valor                          |
      | tipo          | PERCENTUAL                     |
      | valor         | 20                             |
      | data_inicio   | 2025-01-01                     |
      | data_fim      | 2025-12-31                     |
      | uso_por_cliente| 1                             |
    And o pedido "PEDIDO123" tem valor total de "100,00"
    When eu envio uma requisição POST para "/api/pagamento/aplicar-cupom"
    And o corpo contém:
      | campo         | valor                          |
      | pedido_id     | PEDIDO123                      |
      | cupom_codigo  | DESCE20                        |
    Then o status deve ser 200 OK
    And o response deve conter:
      | campo            | valor    |
      | desconto_aplicado| 20.00    |
      | valor_final      | 80.00    |
      | cupom_valido     | true     |

  Cenário 2: Calcular desconto máximo por tipo de cupom
    Examples:
      | tipo        | valor | valor_pedido | desconto_esperado |
      | PERCENTUAL  | 20    | 100.00       | 20.00             |
      | PERCENTUAL  | 50    | 100.00       | 50.00             |
      | FIXO        | 15.00 | 100.00       | 15.00             |
      | FRETE_GRATIS| 0     | 100.00       | 15.00             |
    
    Given existe um cupom do tipo "<tipo>" com valor "<valor>"
    And o pedido tem valor total "<valor_pedido>" e frete "15.00"
    When eu aplico o cupom
    Then o desconto calculado deve ser "<desconto_esperado>"

  Cenário 3: Regras de negócio - cupom já utilizado
    Given o cliente "cli_123" já usou o cupom "DESCE20" no pedido "PEDIDO999"
    And o cupom permite apenas 1 uso por cliente
    When eu tento aplicar o cupom "DESCE20" no pedido "PEDIDO456"
    Then o status deve ser "422 UNPROCESSABLE ENTITY"
    And a mensagem deve ser "Cupom já utilizado por este cliente"

  Cenário 4: Criar promoção via API (admin)
    Given o usuário admin está autenticado
    When eu envio uma requisição POST para "/api/admin/promocoes"
    And o corpo contém dados válidos da promoção:
      | campo         | valor                          |
      | tipo          | PERCENTUAL                     |
      | valor         | 20                             |
      | data_inicio   | 2025-01-01                     |
      | data_fim      | 2025-12-31                     |
      | uso_por_cliente| 1                             |
    Then o status deve ser "201 CREATED"
    And a promoção deve estar com status "ATIVA"