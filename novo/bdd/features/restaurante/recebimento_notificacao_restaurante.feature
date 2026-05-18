Feature: Recebimento de notificação do pedido
  Como proprietário de um restaurante
  Quero poder receber notificação do recebimento de novo pedido
  Para poder confeccioná-los e entregá-los

  Background:
    Given que o restaurante está logado como "dono" no sistema
    And que o restaurante está conectado "via Socket"

  Scenario: Aceite de pedido via notificação
    Given que um aviso de novo pedido apareceu na interface
    When eu seleciono a opção "Aceitar"
    Then o status do pedido deve ser atualizado para "Aceito"

  Scenario: Recusa de pedido via notificação
    Given que uma notificação de pedido está visível
    When eu seleciono a opção "Recusar"
    Then a notificação deve ser fechada e o pedido cancelado
