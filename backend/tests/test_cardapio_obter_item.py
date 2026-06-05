import pytest
from pytest_bdd import scenario, given, when, then, parsers
from fastapi.testclient import TestClient
from fastapi import FastAPI

from modulos.cardapio.rotas import router as cardapio_router
import modulos.cardapio.controle as controle


@scenario("../../bdd/backend/features/cardapio/obter_item.feature", "Obter item do cardápio por ID")
def test_obter_item_cardapio():
    pass


@pytest.fixture
def client():
    test_app = FastAPI()
    test_app.include_router(cardapio_router, prefix="/api/v1")
    return TestClient(test_app)


@pytest.fixture
def context():
    return {}


@given(parsers.parse('o CardapioService retorna um item com id "{item_id}", nome "{nome}" e preço "{preco}"'))
def cardapio_service_retorna_item(item_id, nome, preco, monkeypatch):
    def fake_obter_item(received_id):
        return {
            "item": {
                "id": item_id,
                "nome": nome,
                "preco": preco
            }
        }

    monkeypatch.setattr(controle.CardapioControle, "obter_item", staticmethod(fake_obter_item))
    return {"item_id": item_id, "nome": nome, "preco": preco}


@when(parsers.parse('uma requisição "{method}" for enviada para "{path}"'))
def enviar_requisicao(method, path, client, context):
    if method.upper() == "GET":
        response = client.get(path)
    else:
        raise ValueError(f"Método HTTP não suportado: {method}")

    context["response"] = response


@then(parsers.parse('o status da resposta deve ser "{status_code}"'))
def verificar_status(status_code, context):
    response = context["response"]
    assert str(response.status_code) == status_code


@then(parsers.parse('o JSON da resposta deve conter id "{item_id}"'))
def verificar_json_id(item_id, context):
    body = context["response"].json()
    assert str(body.get("id")) == item_id


@then(parsers.parse('o JSON da resposta deve conter nome "{nome}"'))
def verificar_json_nome(nome, context):
    body = context["response"].json()
    assert body.get("nome") == nome


@then(parsers.parse('o JSON da resposta deve conter preço "{preco}"'))
def verificar_json_preco(preco, context):
    body = context["response"].json()
    assert str(body.get("preco")) == preco