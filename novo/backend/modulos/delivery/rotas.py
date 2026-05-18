from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4

from modulos.delivery.domain.enums import DelivererStatus, OrderStatus
from modulos.delivery.domain.entities import Deliverer, Order
from modulos.delivery.infrastructure.models.deliverers_model import DelivererModel, OrderModel

router = APIRouter(prefix="/delivery", tags=["Delivery"])

# ==================== Pydantic Models ====================

class DelivererCreate(BaseModel):
    name: str
    phone: str
    region: str

class DelivererResponse(BaseModel):
    id: str
    name: str
    phone: str
    region: str
    status: str

class DelivererStatusUpdate(BaseModel):
    status: str

class OrderAssignRequest(BaseModel):
    order_id: str
    region: str
    deliverer_id: Optional[str] = None

class OrderReassignRequest(BaseModel):
    reason: str = "timeout"

class OrderResponse(BaseModel):
    order_id: str
    status: str
    assigned_deliverer_id: Optional[str] = None

# ==================== DELIVERERS ENDPOINTS ====================

@router.get("/deliverers/", status_code=200, response_model=dict)
async def list_deliverers(
    status: Optional[str] = None,
    region: Optional[str] = None
) -> dict:
    """
    List deliverers with optional filters.
    Query params:
    - status: AVAILABLE, OCCUPIED, OFFLINE
    - region: filter by region name
    """
    try:
        filters = {}
        if status:
            # Validate status
            try:
                DelivererStatus(status)
                filters['status'] = status
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid status filter")
        
        if region:
            filters['region'] = region
        
        # Get from database
        query = DelivererModel.objects.all()
        if filters:
            query = query.filter(**filters)
        
        deliverers = [
            {
                'id': str(d.id),
                'name': d.name,
                'phone': d.phone,
                'region': d.region,
                'status': d.status,
            }
            for d in query
        ]
        
        return {'items': deliverers}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/deliverers/", status_code=201, response_model=DelivererResponse)
async def create_deliverer(data: DelivererCreate) -> DelivererResponse:
    """
    Register a new deliverer.
    Required fields: name, phone, region
    """
    try:
        # Validate
        if not data.name or not data.phone or not data.region:
            raise HTTPException(status_code=400, detail="name, phone and region are required")
        
        # Create
        deliverer = DelivererModel.objects.create(
            name=data.name,
            phone=data.phone,
            region=data.region,
            status='AVAILABLE'
        )
        
        return DelivererResponse(
            id=str(deliverer.id),
            name=deliverer.name,
            phone=deliverer.phone,
            region=deliverer.region,
            status=deliverer.status
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/deliverers/{deliverer_id}/status/", status_code=200, response_model=dict)
async def update_deliverer_status(
    deliverer_id: UUID,
    data: DelivererStatusUpdate
) -> dict:
    """
    Update deliverer status.
    Status options: AVAILABLE, OCCUPIED, OFFLINE
    """
    try:
        # Validate status
        try:
            DelivererStatus(data.status)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status value")
        
        # Get and update deliverer
        deliverer = DelivererModel.objects.get(id=deliverer_id)
        deliverer.status = data.status
        deliverer.save()
        
        return {
            'id': str(deliverer.id),
            'status': deliverer.status
        }
    
    except DelivererModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Deliverer not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== ORDERS ENDPOINTS ====================

@router.post("/orders/assign/", status_code=200, response_model=OrderResponse)
async def assign_order(data: OrderAssignRequest) -> OrderResponse:
    """
    Assign a deliverer to an order.
    - If deliverer_id provided: manual assignment
    - If not provided: automatic assignment (find available in region)
    """
    try:
        # Validate
        if not data.order_id or not data.region:
            raise HTTPException(status_code=400, detail="order_id and region are required")
        
        order_id = UUID(data.order_id)
        
        # Get or create order
        order, created = OrderModel.objects.get_or_create(
            id=order_id,
            defaults={'region': data.region, 'status': 'PENDING'}
        )
        
        if data.deliverer_id:
            # Manual assignment
            deliverer_id = UUID(data.deliverer_id)
            deliverer = DelivererModel.objects.get(id=deliverer_id)
            
            if deliverer.status != 'AVAILABLE':
                raise HTTPException(status_code=400, detail="Deliverer is not available")
            
            order.assigned_deliverer_id = deliverer_id
            order.status = 'IN_DELIVERY'
            deliverer.status = 'OCCUPIED'
            deliverer.save()
        else:
            # Automatic assignment
            deliverer = DelivererModel.objects.filter(
                region=data.region,
                status='AVAILABLE'
            ).first()
            
            if not deliverer:
                raise HTTPException(status_code=400, detail="No available deliverer in region")
            
            order.assigned_deliverer_id = deliverer.id
            order.status = 'IN_DELIVERY'
            deliverer.status = 'OCCUPIED'
            deliverer.save()
        
        order.save()
        
        return OrderResponse(
            order_id=str(order.id),
            status=order.status,
            assigned_deliverer_id=str(order.assigned_deliverer_id) if order.assigned_deliverer_id else None
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/orders/{order_id}/reassign/", status_code=200, response_model=OrderResponse)
async def reassign_order(order_id: UUID, data: OrderReassignRequest) -> OrderResponse:
    """
    Reassign an order to another deliverer.
    Reason: 'timeout', 'refused', etc.
    """
    try:
        # Get order
        order = OrderModel.objects.get(id=order_id)
        
        # Free current deliverer
        if order.assigned_deliverer_id:
            current_deliverer = DelivererModel.objects.get(id=order.assigned_deliverer_id)
            current_deliverer.status = 'AVAILABLE'
            current_deliverer.save()
        
        # Find new deliverer
        new_deliverer = DelivererModel.objects.filter(
            region=order.region,
            status='AVAILABLE'
        ).first()
        
        if not new_deliverer:
            raise HTTPException(status_code=400, detail="No available deliverer in region for reassignment")
        
        # Assign
        order.assigned_deliverer_id = new_deliverer.id
        order.status = 'IN_DELIVERY'
        new_deliverer.status = 'OCCUPIED'
        new_deliverer.save()
        order.save()
        
        return OrderResponse(
            order_id=str(order.id),
            status=order.status,
            assigned_deliverer_id=str(order.assigned_deliverer_id) if order.assigned_deliverer_id else None
        )
    
    except OrderModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
