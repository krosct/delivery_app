import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from modulos.cardapio.rotas import router as cardapio_router
import modulos.cardapio.controle as controle


class TestCardapioIntegracao:

    @pytest.fixture
    def client(self):
        test_app = FastAPI()
        test_app.include_router(cardapio_router, prefix="/api/v1")
        return TestClient(test_app)

    def _mockar_conexao_com_item(self, item_id=101, nome="Pizza Calabresa", preco=45.90):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = {
            "id": item_id,
            "nome": nome,
            "preco": preco,
            "descricao": "Pizza salgada deliciosa",
            "categoria": "Pizzas",
            "id_restaurante": 1,
            "disponivel": True,
            "criado_em": "2026-06-04 10:00:00"
        }
        
        mock_conn.cursor.return_value = mock_cursor
        return mock_conn

    @patch('modulos.cardapio.controle.ConexaoBanco.get_connection')
    def test_obter_item_cardapio_sucesso(self, mock_get_connection, client):

        mock_get_connection.return_value = self._mockar_conexao_com_item(
            item_id=101, 
            nome="Pizza Calabresa", 
            preco=45.90
        )
        
        response = client.get("/api/v1/cardapio/101")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 101
        assert data["nome"] == "Pizza Calabresa"
        assert data["preco"] == 45.90
        assert data["categoria"] == "Pizzas"

    @patch('modulos.cardapio.controle.ConexaoBanco.get_connection')
    def test_obter_item_cardapio_nao_encontrado(self, mock_get_connection, client):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        
        response = client.get("/api/v1/cardapio/999")
        
        assert response.status_code == 404
        data = response.json()
        assert "erro" in data["detail"].lower() or "não encontrado" in data["detail"].lower()

    @patch('modulos.cardapio.controle.ConexaoBanco.get_connection')
    def test_obter_multiplos_itens_sequencial(self, mock_get_connection, client):

        def mock_fetchone_side_effect():
            items = [
                {"id": 1, "nome": "Pizza Margherita", "preco": 35.00, "categoria": "Pizzas", 
                 "descricao": "Pizza clássica", "id_restaurante": 1, "disponivel": True, "criado_em": "2026-06-04"},
                {"id": 2, "nome": "Refrigerante", "preco": 5.00, "categoria": "Bebidas",
                 "descricao": "Refrigerante gelado", "id_restaurante": 1, "disponivel": True, "criado_em": "2026-06-04"}
            ]
            for item in items:
                yield item
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = mock_fetchone_side_effect()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        
        response1 = client.get("/api/v1/cardapio/1")
        assert response1.status_code == 200
        assert response1.json()["nome"] == "Pizza Margherita"
        
        response2 = client.get("/api/v1/cardapio/2")
        assert response2.status_code == 200
        assert response2.json()["nome"] == "Refrigerante"