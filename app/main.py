from fastapi import FastAPI, HTTPException
from app.database import init_db
from app.schemas import Pet, PetCreate
from app import models

app = FastAPI(
    title="PetStore API",
    description="Implementación RESTful basada en OpenAPI PetStore",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    init_db()

@app.post("/pet", response_model=Pet, status_code=201)
def add_pet(pet: PetCreate):
    pet_id = models.create_pet(pet.name, pet.status)
    return {"id": pet_id, "name": pet.name, "status": pet.status}

@app.get("/pet/{pet_id}", response_model=Pet)
def get_pet(pet_id: int):
    pet = models.get_pet(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return dict(pet)

@app.get("/pet", response_model=list[Pet])
def list_pets():
    pets = models.list_pets()
    return [dict(p) for p in pets]
