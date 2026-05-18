# SLIDE 4: Rotas e APIs — Especificação Completa

## 📡 Visão Geral dos Endpoints

### Delivery Module — Implementado e Testado ✅

| Método | Endpoint | Status | Testes |
|--------|----------|--------|--------|
| **GET** | `/api/v1/delivery/deliverers/` | ✅ | `test_list_deliverers_all` |
| **GET** | `/api/v1/delivery/deliverers/?status=AVAILABLE` | ✅ | `test_list_deliverers_filter_status` |
| **GET** | `/api/v1/delivery/deliverers/?region=Zona%20Sul` | ✅ | `test_list_deliverers_filter_region` |
| **POST** | `/api/v1/delivery/deliverers/` | ✅ | `test_create_deliverer_success` |
| **PATCH** | `/api/v1/delivery/deliverers/{id}/status/` | ✅ | `test_update_deliverer_status_success` |
| **POST** | `/api/v1/delivery/orders/assign/` | ✅ | `test_assign_order_automatic_success` |
| **POST** | `/api/v1/delivery/orders/{id}/reassign/` | ✅ | `test_reassign_order_success` |

---

## 🔀 Fluxos Operacionais — Detalhados

### FLUXO 1: Registrar Novo Entregador

**Endpoint**: `POST /api/v1/delivery/deliverers/`

**Request**:
```json
{
  "name": "Ana Silva",
  "phone": "11987654321",
  "region": "Zona Sul"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Ana Silva",
  "phone": "11987654321",
  "region": "Zona Sul",
  "status": "AVAILABLE",
  "created_at": "2025-05-18T10:30:00Z"
}
```

**Validações**:
- `name`: obrigatório, string, min 3 caracteres
- `phone`: obrigatório, string, formato validado
- `region`: obrigatório, string válida (Zona Sul, Zona Norte, etc)

**Erros Possíveis**:
```json
// 400 Bad Request — campo obrigatório faltando
{
  "error": "Field 'name' is required"
}

// 400 Bad Request — validação falhou
{
  "error": "Phone format invalid"
}
```

---

### FLUXO 2: Listar Entregadores com Filtros

**Endpoint**: `GET /api/v1/delivery/deliverers/`

**Query Parameters** (opcionais):
- `status`: `AVAILABLE`, `OCCUPIED`, `OFFLINE`
- `region`: `Zona Sul`, `Zona Norte`, `Centro`, `Leste`, `Oeste`

**Exemplos**:
```
GET /api/v1/delivery/deliverers/
GET /api/v1/delivery/deliverers/?status=AVAILABLE
GET /api/v1/delivery/deliverers/?region=Zona%20Sul
GET /api/v1/delivery/deliverers/?status=AVAILABLE&region=Zona%20Norte
```

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Ana Silva",
      "phone": "11987654321",
      "region": "Zona Sul",
      "status": "AVAILABLE"
    },
    {
      "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
      "name": "Bruno Costa",
      "phone": "11912345678",
      "region": "Centro",
      "status": "OCCUPIED"
    }
  ],
  "count": 2
}
```

**Lógica de Filtro**:
```python
deliverers = DelivererModel.objects.all()

if status:
    deliverers = deliverers.filter(status=status)

if region:
    deliverers = deliverers.filter(region=region)

return {"items": [dto(d) for d in deliverers], "count": len(deliverers)}
```

---

### FLUXO 3: Atualizar Status de Entregador

**Endpoint**: `PATCH /api/v1/delivery/deliverers/{deliverer_id}/status/`

**Request**:
```json
{
  "status": "OCCUPIED"
}
```

**Valid Status Values**:
- `AVAILABLE`: pronto para receber pedidos
- `OCCUPIED`: entregando um pedido no momento
- `OFFLINE`: não disponível

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Ana Silva",
  "status": "OCCUPIED",
  "region": "Zona Sul",
  "updated_at": "2025-05-18T10:35:00Z"
}
```

**Erros**:
```json
// 400 Bad Request — status inválido
{
  "error": "Invalid status 'INVALID_STATUS'"
}

// 404 Not Found — entregador não existe
{
  "error": "Deliverer not found"
}
```

---

### FLUXO 4: Atribuir Entregador a Pedido (Automático ou Manual)

**Endpoint**: `POST /api/v1/delivery/orders/assign/`

#### Modo Automático — Sistema escolhe

**Request**:
```json
{
  "order_id": "order-123",
  "region": "Zona Sul"
}
```

**Lógica**:
```python
# 1. Buscar todos os entregadores AVAILABLE na região
available = DelivererModel.objects.filter(
    region=region,
    status='AVAILABLE'
)

# 2. Se nenhum encontrado, erro
if not available:
    raise HTTPException(400, "No available deliverer in region Zona Sul")

# 3. Escolher primeiro (FIFO)
chosen = available[0]

# 4. Atualizar entregador: AVAILABLE → OCCUPIED
chosen.status = 'OCCUPIED'
chosen.save()

# 5. Atualizar pedido: PENDING → IN_DELIVERY
order = OrderModel.objects.get(id=order_id)
order.status = 'IN_DELIVERY'
order.assigned_deliverer_id = chosen.id
order.save()
```

**Response** (200 OK):
```json
{
  "order_id": "order-123",
  "status": "IN_DELIVERY",
  "assigned_deliverer_id": "550e8400-e29b-41d4-a716-446655440000",
  "assigned_deliverer_name": "Ana Silva"
}
```

#### Modo Manual — Client especifica

**Request**:
```json
{
  "order_id": "order-123",
  "region": "Zona Sul",
  "deliverer_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Validações**:
- Deliverer existe?
- Deliverer está na região correta?
- Deliverer está em status AVAILABLE?

**Response** (200 OK):
```json
{
  "order_id": "order-123",
  "status": "IN_DELIVERY",
  "assigned_deliverer_id": "550e8400-e29b-41d4-a716-446655440000",
  "assigned_deliverer_name": "Ana Silva"
}
```

**Erros Possíveis**:
```json
// 400 Bad Request — nenhum entregador disponível
{
  "error": "No available deliverer in region Zona Sul"
}

// 400 Bad Request — entregador ocupado
{
  "error": "Deliverer is not available"
}

// 404 Not Found — pedido não existe
{
  "error": "Order not found"
}

// 404 Not Found — entregador não existe
{
  "error": "Deliverer not found"
}
```

---

### FLUXO 5: Reatribuir Pedido (após Recusa ou Cancelamento)

**Endpoint**: `POST /api/v1/delivery/orders/{order_id}/reassign/`

**Request**:
```json
{
  "reason": "refused"
}
```

**Valid Reasons**:
- `refused`: entregador recusou o pedido
- `cancelled`: cancelamento por cliente
- `damaged`: pedido danificado
- `other`: outro motivo

**Lógica**:
```python
# 1. Buscar pedido
order = OrderModel.objects.get(id=order_id)

# 2. Marcar entregador anterior como AVAILABLE
old_deliverer = DelivererModel.objects.get(id=order.assigned_deliverer_id)
old_deliverer.status = 'AVAILABLE'
old_deliverer.save()

# 3. Buscar novo entregador AVAILABLE na mesma região
available = DelivererModel.objects.filter(
    region=order.region,
    status='AVAILABLE'
)

if not available:
    raise HTTPException(400, "No available deliverer for reassignment")

# 4. Atribuir novo
new_deliverer = available[0]
new_deliverer.status = 'OCCUPIED'
new_deliverer.save()

# 5. Atualizar pedido (continua IN_DELIVERY)
order.assigned_deliverer_id = new_deliverer.id
order.reassign_reason = reason
order.reassigned_count += 1
order.save()
```

**Response** (200 OK):
```json
{
  "order_id": "order-123",
  "status": "IN_DELIVERY",
  "previous_deliverer_id": "550e8400-e29b-41d4-a716-446655440000",
  "new_deliverer_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "new_deliverer_name": "Bruno Costa",
  "reason": "refused",
  "reassigned_count": 1
}
```

**Erros**:
```json
// 400 Bad Request — motivo inválido
{
  "error": "Invalid reason"
}

// 400 Bad Request — nenhum entregador para reatribução
{
  "error": "No available deliverer for reassignment"
}

// 404 Not Found
{
  "error": "Order not found"
}
```

---

## 📊 Request/Response Payload Schemas

### DelivererDTO (Data Transfer Object)

```json
{
  "id": "uuid",
  "name": "string (3-100 chars)",
  "phone": "string (formatted)",
  "region": "string (Zona Sul|Zona Norte|Centro|Leste|Oeste)",
  "status": "string (AVAILABLE|OCCUPIED|OFFLINE)",
  "created_at": "ISO8601 datetime",
  "updated_at": "ISO8601 datetime"
}
```

### OrderDTO

```json
{
  "id": "uuid",
  "status": "string (PENDING|IN_DELIVERY|DELIVERED|CANCELLED)",
  "region": "string",
  "assigned_deliverer_id": "uuid (nullable)",
  "assigned_deliverer_name": "string (nullable)",
  "reassigned_count": "integer",
  "created_at": "ISO8601 datetime"
}
```

### ErrorResponse

```json
{
  "error": "string (description)",
  "timestamp": "ISO8601 datetime",
  "path": "string (request path)",
  "method": "string (HTTP method)"
}
```

---

## 🔒 Validações e Constraints

### Validações de Negócio

| Regra | Implementação |
|-------|-------------------|
| Nenhum entregador pode ter 2 pedidos simultâneos | OCCUPIED → max 1 order |
| Pedidos só podem ser atribuídos a entregador AVAILABLE | Check status == 'AVAILABLE' |
| Reatribuição só dentro da mesma região | Filter by order.region |
| Reatribuição impossível sem entregador disponível | Return 400 error |
| Nome entregador não pode ser vazio | Validate len > 0 |
| Phone format deve ser válido | Regex validation |
| Region deve estar em lista pré-definida | Enum check |

### Constraints de Dados

```sql
-- Deliverer
ALTER TABLE delivery_deliverer 
  ADD CONSTRAINT chk_status 
  CHECK (status IN ('AVAILABLE', 'OCCUPIED', 'OFFLINE'));

ALTER TABLE delivery_deliverer 
  ADD CONSTRAINT chk_region 
  CHECK (region IN ('Zona Sul', 'Zona Norte', 'Centro', 'Leste', 'Oeste'));

-- Order
ALTER TABLE delivery_order 
  ADD CONSTRAINT chk_order_status 
  CHECK (status IN ('PENDING', 'IN_DELIVERY', 'DELIVERED', 'CANCELLED'));

ALTER TABLE delivery_order 
  ADD CONSTRAINT fk_deliverer 
  FOREIGN KEY (assigned_deliverer_id) REFERENCES delivery_deliverer(id);
```

---

## ✅ Cobertura de Testes

| Cenário | Teste | Status |
|---------|-------|--------|
| Criar entregador com dados válidos | `test_create_deliverer_success` | ✅ |
| Criar entregador com campos faltando | `test_create_deliverer_missing_fields` | ✅ |
| Listar todos os entregadores | `test_list_deliverers_all` | ✅ |
| Listar com filtro de status | `test_list_deliverers_filter_status` | ✅ |
| Listar com filtro de região | `test_list_deliverers_filter_region` | ✅ |
| Atualizar status com valor válido | `test_update_deliverer_status_success` | ✅ |
| Atualizar com status inválido | `test_update_deliverer_invalid_status` | ✅ |
| Atribuir automaticamente (sucesso) | `test_assign_order_automatic_success` | ✅ |
| Atribuir manualmente (sucesso) | `test_assign_order_manual_success` | ✅ |
| Atribuir sem entregador disponível | `test_assign_order_no_available_deliverer` | ✅ |
| Atribuir a entregador ocupado | `test_assign_order_unavailable_deliverer` | ✅ |
| Reatribuir com sucesso | `test_reassign_order_success` | ✅ |

---

## 🎯 Exemplo de Fluxo Completo (Happy Path)

```
1. POST /api/v1/delivery/deliverers/
   ↓
   {"name": "Ana", "phone": "...", "region": "Zona Sul"}
   ↓
   201 Created + {"id": "uuid-ana", "status": "AVAILABLE"}

2. GET /api/v1/delivery/deliverers/?region=Zona%20Sul
   ↓
   200 OK + {"items": [{"id": "uuid-ana", ...}]}

3. POST /api/v1/delivery/orders/assign/
   ↓
   {"order_id": "order-123", "region": "Zona Sul"}
   ↓
   200 OK + {"order_id": "order-123", "status": "IN_DELIVERY", "assigned_deliverer_id": "uuid-ana"}

4. GET /api/v1/delivery/deliverers/?region=Zona%20Sul
   ↓
   200 OK + {"items": [{"id": "uuid-ana", "status": "OCCUPIED"}]}

5. POST /api/v1/delivery/orders/order-123/reassign/
   ↓
   {"reason": "refused"}
   ↓
   200 OK + {"order_id": "order-123", "new_deliverer_id": "..."}

6. PATCH /api/v1/delivery/deliverers/uuid-ana/status/
   ↓
   {"status": "OFFLINE"}
   ↓
   200 OK + {"id": "uuid-ana", "status": "OFFLINE"}
```

---

## 📝 Notas Técnicas

### Stack Tecnológico
- **Framework HTTP**: FastAPI 0.104.1
- **Persistência**: Django ORM 5.2.13
- **Database**: PostgreSQL (produção) / SQLite (testes)
- **Validation**: Pydantic v2
- **Testing**: pytest 9.0.3 + pytest-bdd 8.1.0

### Deployment
```bash
# Instalar dependências
pip install fastapi django djangorestframework pydantic

# Executar servidor
python manage.py migrate
uvicorn novo.backend.main:app --host 0.0.0.0 --port 8000

# Executar testes
PYTHONPATH=novo/backend pytest novo/bdd/features/steps/ -v
```

---

**Documentação**: Slide 4 — Rotas e APIs  
**Data**: 2025-05-18  
**Status**: ✅ Pronto para Apresentação
