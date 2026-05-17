Feature: Envio de comprovantes por email - BACKEND

  Cenário 1: Gerar comprovante em JSON/PDF via API
    Given o pedido "PEDIDO123" foi finalizado
    When eu envio uma requisição GET para "/api/pagamento/comprovante/PEDIDO123"
    Then o status deve ser "200 OK"
    And o Content-Type deve ser "application/json" ou "application/pdf"
    And o comprovante deve conter:
      | campo               | valor                          |
      | numero_pedido       | PEDIDO123                      |
      | itens               | [{"nome":"Pizza","qtd":2}]     |
      | valor_total         | 100.00                         |
      | forma_pagamento     | CREDIT_CARD                    |
      | restaurante_nome    | Pizzaria do Zé                 |

  Cenário 2: Disparo assíncrono de email
    Given o pedido "PEDIDO123" foi finalizado
    And o email do cliente é "cliente@email.com"
    When o pedido é confirmado
    Then um job deve ser enfileirado para envio de email
    And o email deve conter o comprovante gerado
    And o assunto deve ser "Comprovante do seu pedido #PEDIDO123"