# language: pt

Feature: Gerenciamento de métodos de pagamento - BACKEND

  Como um sistema
  Eu quero validar as regras de negócio de métodos de pagamento
  Para garantir a integridade dos dados

  # Cenário 1: API de criação
  Scenario: Criar novo método de pagamento via API
    Given o cliente com ID "cli_123" está autenticado
    And o token JWT é válido
    When eu envio uma requisição POST para "/api/pagamento/metodos"
    And o corpo da requisição contém:
      | campo         | valor                          |
      | tipo          | CREDIT_CARD                    |
      | numero        | 4111111111111111               |
      | nome_titular  | JOAO SILVA                     |
      | validade_mes  | 12                             |
      | validade_ano  | 2028                           |
      | cvv           | 123                            |
    Then o status da resposta deve ser "201 CREATED"
    And o método de pagamento deve estar associado ao cliente "cli_123"

  # Cenário 2: Validação de dados inválidos
  Scenario: Tentar criar método com cartão expirado via API
    Given o cliente com ID "cli_123" está autenticado
    When eu envio uma requisição POST para "/api/pagamento/metodos"
    And o corpo da requisição contém:
      | campo         | valor                          |
      | tipo          | CREDIT_CARD                    |
      | numero        | 4111111111111111               |
      | nome_titular  | JOAO SILVA                     |
      | validade_mes  | 12                             |
      | validade_ano  | 2020                           |
      | cvv           | 123                            |
    Then o status da resposta deve ser "422 UNPROCESSABLE ENTITY"
    And a mensagem deve ser "Data de validade expirada"

  # Cenário 3: API de remoção
  Scenario: Remover método de pagamento via API
    Given o cliente "cli_123" possui o método "metodo_456" cadastrado
    When eu envio uma requisição DELETE para "/api/pagamento/metodos/metodo_456"
    Then o status da resposta deve ser "204 NO CONTENT"
    And ao buscar os métodos do cliente "cli_123", "metodo_456" não deve mais existir

  # Cenário 5: API de atualização
  Scenario: Atualizar dados do método de pagamento via API
    Given o cliente "cli_123" possui o método "metodo_456"
    And a validade do método "metodo_456" é "12/2025"
    When eu envio uma requisição PUT para "/api/pagamento/metodos/metodo_456"
    And o corpo contém:
      | campo         | valor    |
      | validade_mes  | 06       |
      | validade_ano  | 2027    |
    Then o status deve ser "200 OK"
    And a validade do método deve ser atualizada para "06/2027"