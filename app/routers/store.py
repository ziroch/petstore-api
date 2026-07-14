from typing import Dict
from fastapi import APIRouter, HTTPException, status

from app.models import Order


router = APIRouter(prefix="/store", tags=["store"])


@router.get("/inventory", response_model=Dict[str, int])
def get_inventory():
    """Returns pet inventories by status"""
    from app.database import db
    return db.get_inventory()


@router.post("/order", response_model=Order, status_code=status.HTTP_200_OK)
def place_order(order: Order):
    """Place an order for a pet"""
    from app.database import db
    order_id = db.create_order(order.model_dump(exclude_unset=True))
    return db.get_order(order_id)


@router.get("/order/{orderId}", response_model=Order)
def get_order_by_id(orderId: int):
    """Find purchase order by ID"""
    from app.database import db
    order = db.get_order(orderId)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/order/{orderId}")
def delete_order(orderId: int):
    """Delete purchase order by ID"""
    from app.database import db
    if not db.delete_order(orderId):
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted"}
