Feature: GUI de entregadores

  Scenario Outline: cadastrar entregador com sucesso
    Given eu estou na tela de entregadores
    When eu cadastro o entregador "<name>"
    Then vejo "<name>" na lista de entregadores

    Examples:
      | name  |
      | Ana   |
      | Bruno |