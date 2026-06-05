import pytest
from unittest.mock import Mock, patch, MagicMock
from modulos.cardapio.controle import CardapioControle


class TestCardapioControleValidacoes:

    def _criar_mock_conexao(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.side_effect = [
            {'id': 1},  
            None  
        ]
        
        mock_conn.cursor.return_value = mock_cursor
        return mock_conn

    @patch('modulos.cardapio.controle.ConexaoBanco.get_connection')
    def test_cadastrar_item_campo_obrigatorio_faltando(self, mock_get_connection):
        mock_get_connection.return_value = Mock()
        
        dados = {
            'nome': 'Pizza',
        }
        resultado = CardapioControle.cadastrar_item(dados)
        
        assert "erro" in resultado
        assert resultado["status_code"] == 400
        assert "obrigatório" in resultado["erro"].lower()

    @patch('modulos.cardapio.controle.ConexaoBanco.get_connection')
    def test_cadastrar_item_preco_negativo(self, mock_get_connection):
        mock_get_connection.return_value = self._criar_mock_conexao()
        
        dados = {
            'nome': 'Pizza Calabresa',
            'descricao': 'Pizza salgada',
            'preco': -10.0,  
            'categoria': 'Pizzas',
            'id_restaurante': 1
        }
        resultado = CardapioControle.cadastrar_item(dados)
        
        assert "erro" in resultado
        assert resultado["status_code"] == 400
        assert "negativo" in resultado["erro"].lower()

    @patch('modulos.cardapio.controle.ConexaoBanco.get_connection')
    def test_cadastrar_item_preco_invalido(self, mock_get_connection):
        mock_get_connection.return_value = self._criar_mock_conexao()
        
        dados = {
            'nome': 'Pizza Calabresa',
            'descricao': 'Pizza salgada',
            'preco': 'abc',  
            'categoria': 'Pizzas',
            'id_restaurante': 1
        }
        resultado = CardapioControle.cadastrar_item(dados)
        
        assert "erro" in resultado
        assert resultado["status_code"] == 400
        assert "número" in resultado["erro"].lower()