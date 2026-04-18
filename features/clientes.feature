Feature: Gerenciamento de clientes

  Como um usuário do sistema de delivery
  Eu quero gerenciar os clientes cadastrados
  Para manter seus dados organizados e acessíveis durante o uso do sistema

  Scenario: Cadastro de um novo cliente com sucesso
    Given que o usuário está na tela de cadastro de clientes
    When ele informa nome, telefone e endereço válidos
    And confirma o cadastro
    Then o cliente deve ser registrado no sistema com sucesso

  Scenario: Falha ao cadastrar cliente com dados incompletos
    Given que o usuário está na tela de cadastro de clientes
    When ele tenta cadastrar um cliente sem informar o telefone
    Then o sistema deve exibir uma mensagem de erro informando que o telefone é obrigatório