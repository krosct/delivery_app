Feature: Deliverer BDD

  Scenario Outline: cadastrar entregador com sucesso
    Given nenhum entregador existe
    When eu cadastro um entregador com nome "<name>" telefone "<phone>" regiao "<region>"
    Then o entregador "<name>" deve ficar com status "<status>"

    Examples:
      | name  | phone        | region   | status    |
      | Ana   | 11999999999  | Zona Sul | AVAILABLE |
      | Bruno | 11888888888  | Centro    | AVAILABLE |