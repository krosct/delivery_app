"""
Testes de API para o módulo de Delivery.
Complementa os BDD tests com testes unitários de endpoints específicos.
"""
import json
import pytest
from uuid import uuid4
from django.test import Client

from modulos.delivery.domain.enums import DelivererStatus, OrderStatus
from modulos.delivery.infrastructure.models.deliverers_model import DelivererModel, OrderModel


@pytest.mark.django_db
class TestDeliverersAPI:
    """Testes para endpoints de entregadores."""
    
    def test_create_deliverer_success(self):
        """POST /api/v1/delivery/deliverers/ - Criar entregador com sucesso."""
        client = Client()
        
        response = client.post(
            '/api/v1/delivery/deliverers/',
            data=json.dumps({
                'name': 'João Silva',
                'phone': '11987654321',
                'region': 'Centro'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data['name'] == 'João Silva'
        assert data['status'] == 'AVAILABLE'
        assert data['region'] == 'Centro'
    
    def test_create_deliverer_missing_fields(self):
        """POST /api/v1/delivery/deliverers/ - Erro quando faltam campos."""
        client = Client()
        
        response = client.post(
            '/api/v1/delivery/deliverers/',
            data=json.dumps({'name': 'João'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
    
    def test_list_deliverers_all(self):
        """GET /api/v1/delivery/deliverers/ - Listar todos os entregadores."""
        client = Client()
        
        # Criar alguns entregadores
        DelivererModel.objects.create(
            name='Ana', phone='11111111111', region='Sul', status='AVAILABLE'
        )
        DelivererModel.objects.create(
            name='Bruno', phone='22222222222', region='Norte', status='OCCUPIED'
        )
        
        response = client.get('/api/v1/delivery/deliverers/')
        
        assert response.status_code == 200
        data = response.json()
        assert len(data['items']) == 2
    
    def test_list_deliverers_filter_status(self):
        """GET /api/v1/delivery/deliverers/?status=AVAILABLE - Filtrar por status."""
        client = Client()
        
        DelivererModel.objects.create(
            name='Ana', phone='11111111111', region='Sul', status='AVAILABLE'
        )
        DelivererModel.objects.create(
            name='Bruno', phone='22222222222', region='Norte', status='OCCUPIED'
        )
        
        response = client.get('/api/v1/delivery/deliverers/?status=AVAILABLE')
        
        assert response.status_code == 200
        data = response.json()
        assert len(data['items']) == 1
        assert data['items'][0]['status'] == 'AVAILABLE'
    
    def test_list_deliverers_filter_region(self):
        """GET /api/v1/delivery/deliverers/?region=Sul - Filtrar por região."""
        client = Client()
        
        DelivererModel.objects.create(
            name='Ana', phone='11111111111', region='Sul', status='AVAILABLE'
        )
        DelivererModel.objects.create(
            name='Bruno', phone='22222222222', region='Norte', status='AVAILABLE'
        )
        
        response = client.get('/api/v1/delivery/deliverers/?region=Sul')
        
        assert response.status_code == 200
        data = response.json()
        assert len(data['items']) == 1
        assert data['items'][0]['region'] == 'Sul'
    
    def test_update_deliverer_status_success(self):
        """PATCH /api/v1/delivery/deliverers/{id}/status/ - Atualizar status."""
        client = Client()
        
        deliverer = DelivererModel.objects.create(
            name='Ana', phone='11111111111', region='Sul', status='AVAILABLE'
        )
        
        response = client.patch(
            f'/api/v1/delivery/deliverers/{deliverer.id}/status/',
            data=json.dumps({'status': 'OCCUPIED'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'OCCUPIED'
        
        # Verificar que foi salvo no banco
        updated = DelivererModel.objects.get(id=deliverer.id)
        assert updated.status == 'OCCUPIED'
    
    def test_update_deliverer_invalid_status(self):
        """PATCH /api/v1/delivery/deliverers/{id}/status/ - Status inválido."""
        client = Client()
        
        deliverer = DelivererModel.objects.create(
            name='Ana', phone='11111111111', region='Sul', status='AVAILABLE'
        )
        
        response = client.patch(
            f'/api/v1/delivery/deliverers/{deliverer.id}/status/',
            data=json.dumps({'status': 'INVALID'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data


@pytest.mark.django_db
class TestOrdersAPI:
    """Testes para endpoints de ordens."""
    
    def test_assign_order_automatic_success(self):
        """POST /api/v1/delivery/orders/assign/ - Atribuição automática."""
        client = Client()
        
        # Criar entregador disponível
        deliverer = DelivererModel.objects.create(
            name='Ana', phone='11111111111', region='Sul', status='AVAILABLE'
        )
        
        # Criar ordem
        order = OrderModel.objects.create(
            region='Sul', status='PENDING'
        )
        
        response = client.post(
            '/api/v1/delivery/orders/assign/',
            data=json.dumps({
                'order_id': str(order.id),
                'region': 'Sul'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'IN_DELIVERY'
        assert data['assigned_deliverer_id'] == str(deliverer.id)
        
        # Verificar que entregador está ocupado
        updated_deliverer = DelivererModel.objects.get(id=deliverer.id)
        assert updated_deliverer.status == 'OCCUPIED'
    
    def test_assign_order_manual_success(self):
        """POST /api/v1/delivery/orders/assign/ - Atribuição manual."""
        client = Client()
        
        deliverer = DelivererModel.objects.create(
            name='Bruno', phone='22222222222', region='Norte', status='AVAILABLE'
        )
        
        order = OrderModel.objects.create(
            region='Norte', status='PENDING'
        )
        
        response = client.post(
            '/api/v1/delivery/orders/assign/',
            data=json.dumps({
                'order_id': str(order.id),
                'region': 'Norte',
                'deliverer_id': str(deliverer.id)
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['assigned_deliverer_id'] == str(deliverer.id)
    
    def test_assign_order_no_available_deliverer(self):
        """POST /api/v1/delivery/orders/assign/ - Erro sem entregador disponível."""
        client = Client()
        
        order = OrderModel.objects.create(
            region='Leste', status='PENDING'
        )
        
        response = client.post(
            '/api/v1/delivery/orders/assign/',
            data=json.dumps({
                'order_id': str(order.id),
                'region': 'Leste'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data or 'detail' in data
    
    def test_assign_order_unavailable_deliverer(self):
        """POST /api/v1/delivery/orders/assign/ - Erro com entregador ocupado."""
        client = Client()
        
        deliverer = DelivererModel.objects.create(
            name='Leo', phone='33333333333', region='Oeste', status='OCCUPIED'
        )
        
        order = OrderModel.objects.create(
            region='Oeste', status='PENDING'
        )
        
        response = client.post(
            '/api/v1/delivery/orders/assign/',
            data=json.dumps({
                'order_id': str(order.id),
                'region': 'Oeste',
                'deliverer_id': str(deliverer.id)
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data or 'detail' in data
    
    def test_reassign_order_success(self):
        """POST /api/v1/delivery/orders/{id}/reassign/ - Reatribuir ordem."""
        client = Client()
        
        # Criar dois entregadores
        d1 = DelivererModel.objects.create(
            name='Ana', phone='11111111111', region='Sul', status='OCCUPIED'
        )
        d2 = DelivererModel.objects.create(
            name='Bruno', phone='22222222222', region='Sul', status='AVAILABLE'
        )
        
        # Criar ordem atribuída a d1
        order = OrderModel.objects.create(
            region='Sul',
            status='IN_DELIVERY',
            assigned_deliverer_id=d1.id
        )
        
        response = client.post(
            f'/api/v1/delivery/orders/{order.id}/reassign/',
            data=json.dumps({'reason': 'timeout'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.json()
        # Deve ter sido atribuído a d2
        assert data['assigned_deliverer_id'] == str(d2.id)
        
        # Verificar que d1 agora está disponível
        updated_d1 = DelivererModel.objects.get(id=d1.id)
        assert updated_d1.status == 'AVAILABLE'
        
        # Verificar que d2 agora está ocupado
        updated_d2 = DelivererModel.objects.get(id=d2.id)
        assert updated_d2.status == 'OCCUPIED'
