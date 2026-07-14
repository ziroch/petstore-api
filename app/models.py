from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class OrderStatus(str, Enum):
    placed = "placed"
    approved = "approved"
    delivered = "delivered"


class PetStatus(str, Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


# ─── Category ─────────────────────────────────────
class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


# ─── Tag ──────────────────────────────────────────
class Tag(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


# ─── Pet ──────────────────────────────────────────
class Pet(BaseModel):
    id: Optional[int] = None
    category: Optional[Category] = None
    name: str
    photoUrls: List[str]
    tags: Optional[List[Tag]] = None
    status: Optional[PetStatus] = None


# ─── Order ────────────────────────────────────────
class Order(BaseModel):
    id: Optional[int] = None
    petId: Optional[int] = None
    quantity: Optional[int] = None
    shipDate: Optional[datetime] = None
    status: Optional[OrderStatus] = None
    complete: Optional[bool] = False


# ─── User ─────────────────────────────────────────
class User(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    userStatus: Optional[int] = None


# ─── ApiResponse ──────────────────────────────────
class ApiResponse(BaseModel):
    code: Optional[int] = None
    type: Optional[str] = None
    message: Optional[str] = None
