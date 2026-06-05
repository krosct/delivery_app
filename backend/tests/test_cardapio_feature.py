import pytest
from pytest_bdd import scenario, given, when, then, parsers
from fastapi.testclient import TestClient
from fastapi import FastAPI

from modulos.cardapio.rotas import router as cardapio_router
import modulos.cardapio.controle as controle


@scenario('../../bdd/backend/features/cardapio/cardapio.feature', 'Obter item do cardápio por ID')
def test_obter_item_cardapio():
    pass


@scenario('../../bdd/backend/features/cardapio/cardapio.feature', 'Cadastrar novo item no cardápio')
def test_cadastrar_item_cardapio():
    pass


@scenario('../../bdd/backend/features/cardapio/cardapio.feature', 'Atualizar preço de um item existente')
def test_atualizar_preco_item_cardapio():
    pass


@scenario('../../bdd/backend/features/cardapio/cardapio.feature', 'Tentar remover item inexistente do cardápio')
def test_remover_item_inexistente_cardapio():
    pass


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(cardapio_router, prefix='/api/v1')
    return TestClient(app)


@pytest.fixture
def context():
    return {}


@given(parsers.parse('o CardapioService retorna um item com id "{item_id}", nome "{nome}" e preço "{preco}"'))
def cardapio_service_retorna_item(item_id, nome, preco, monkeypatch):
    def fake_obter_item(received_id):
        assert str(received_id) == str(item_id)
        return {
            'item': {
                'id': int(item_id),
                'nome': nome,
                'descricao': 'Descrição simulada',
                'preco': float(preco),
                'categoria': 'Simulado',
                'id_restaurante': 1,
                'disponivel': True,
            },
            'status_code': 200,
        }

    monkeypatch.setattr(controle.CardapioControle, 'obter_item', staticmethod(fake_obter_item))


@given(parsers.parse('não existe um item cadastrado com o nome "{nome}"'))
def nao_existe_item_cadastrado(nome, monkeypatch):
    def fake_cadastrar_item(dados):
        return {
            'mensagem': 'Item cadastrado com sucesso',
            'id': 1,
            'status_code': 201,
            'nome': dados.get('nome'),
            'preco': str(dados.get('preco')),
        }

    monkeypatch.setattr(controle.CardapioControle, 'cadastrar_item', staticmethod(fake_cadastrar_item))


@given(parsers.parse('existe um item cadastrado com id "{item_id}" e preço "{preco}"'))
def existe_item_cadastrado(item_id, preco, monkeypatch):
    def fake_atualizar_item(received_id, dados):
        assert str(received_id) == str(item_id)
        return {
            'mensagem': 'Item atualizado com sucesso',
            'id': int(item_id),
            'preco': float(dados.get('preco')),
            'status_code': 200,
        }

    monkeypatch.setattr(controle.CardapioControle, 'atualizar_item', staticmethod(fake_atualizar_item))


@given(parsers.parse('não existe item cadastrado com id "{item_id}"'))
def nao_existe_item_id(item_id, monkeypatch):
    def fake_deletar_item(received_id):
        assert str(received_id) == str(item_id)
        return {
            'erro': 'Item não encontrado',
            'status_code': 404,
        }

    monkeypatch.setattr(controle.CardapioControle, 'deletar_item', staticmethod(fake_deletar_item))


@when(parsers.parse('uma requisição "{method}" for enviada para "{path}"'))
def enviar_requisicao_sem_body(method, path, client, context):
    api_path = path
    if path.startswith('/menu'):
        api_path = path.replace('/menu', '/api/v1/cardapio')
    if method.upper() == 'GET':
        response = client.get(api_path)
    elif method.upper() == 'DELETE':
        response = client.delete(api_path)
    else:
        raise ValueError(f'Método HTTP não suportado: {method}')
    context['response'] = response


@when(parsers.parse('uma requisição "{method}" for enviada para "{path}" contendo nome "{nome}", descrição "{descricao}" e preço "{preco}"'))
def enviar_requisicao_com_body(method, path, nome, descricao, preco, client, context):
    api_path = path
    if path == '/menu':
        api_path = '/api/v1/cardapio/cadastrar'
    payload = {
        'nome': nome,
        'descricao': descricao,
        'preco': float(preco),
        'categoria': 'Lanches',
        'id_restaurante': 1,
    }
    if method.upper() == 'POST':
        response = client.post(api_path, json=payload)
    else:
        raise ValueError(f'Método HTTP não suportado: {method}')
    context['response'] = response


@when(parsers.parse('uma requisição "{method}" for enviada para "{path}" alterando o preço para "{preco}"'))
def enviar_requisicao_atualiza_preco(method, path, preco, client, context):
    api_path = path.replace('/menu', '/api/v1/cardapio')
    payload = {'preco': float(preco)}
    if method.upper() == 'PUT':
        response = client.put(api_path, json=payload)
    else:
        raise ValueError(f'Método HTTP não suportado: {method}')
    context['response'] = response


@then(parsers.parse('o status da resposta deve ser "{status_code}"'))
def verificar_status(status_code, context):
    response = context['response']
    assert str(response.status_code) == status_code, f'Esperado {status_code}, obteve {response.status_code}'


@then(parsers.parse('o JSON da resposta deve conter id "{item_id}"'))
def verificar_json_id(item_id, context):
    body = context['response'].json()
    assert str(body.get('id')) == item_id


@then(parsers.parse('o JSON da resposta deve conter nome "{nome}"'))
def verificar_json_nome(nome, context):
    body = context['response'].json()
    assert body.get('nome') == nome


@then(parsers.parse('o JSON da resposta deve conter preço "{preco}"'))
def verificar_json_preco(preco, context):
    body = context['response'].json()
    actual_price = body.get('preco')
    assert float(actual_price) == float(preco)


@then(parsers.parse('o JSON da resposta deve conter a mensagem "{mensagem}"'))
def verificar_json_mensagem(mensagem, context):
    body = context['response'].json()
    assert mensagem in str(body.get('detail', body.get('mensagem', '')))
