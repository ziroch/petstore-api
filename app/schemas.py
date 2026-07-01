from pydantic import BaseModel
from typing import Optional

class Pet(BaseModel):
    id: Optional[int]
    name: str
    status: str

class PetCreate(BaseModel):
    name: str
    status: str
