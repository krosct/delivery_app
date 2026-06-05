Feature: Cardápio API
    Scenario: Obter item do cardápio por ID
        Given o CardapioService retorna um item com id "101", nome "Pizza Calabresa" e preço "45.90"
        When uma requisição "GET" for enviada para "/api/v1/cardapio/101"
        Then o status da resposta deve ser "200"
        And o JSON da resposta deve conter id "101"
        And o JSON da resposta deve conter nome "Pizza Calabresa"
        And o JSON da resposta deve conter preço "45.90"

    Scenario: Cadastrar novo item no cardápio
        Given não existe um item cadastrado com o nome "Hambúrguer Artesanal"
        When uma requisição "POST" for enviada para "/menu" contendo nome "Hambúrguer Artesanal", descrição "Pão brioche, carne bovina e queijo" e preço "32.50"
        Then o status da resposta deve ser "201"
        And o JSON da resposta deve conter nome "Hambúrguer Artesanal"
        And o JSON da resposta deve conter preço "32.50"

    Scenario: Atualizar preço de um item existente
        Given existe um item cadastrado com id "101" e preço "45.90"
        When uma requisição "PUT" for enviada para "/menu/101" alterando o preço para "49.90"
        Then o status da resposta deve ser "200"
        And o JSON da resposta deve conter id "101"
        And o JSON da resposta deve conter preço "49.90"
        
    Scenario: Tentar remover item inexistente do cardápio
        Given não existe item cadastrado com id "999"
        When uma requisição "DELETE" for enviada para "/menu/999"
        Then o status da resposta deve ser "404"
        And o JSON da resposta deve conter a mensagem "Item não encontrado"
