from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Form, UploadFile, File
from fastapi.responses import JSONResponse

from app.models import Pet, PetStatus, ApiResponse


router = APIRouter(prefix="/pet", tags=["pet"])


@router.post("", response_model=Pet, status_code=status.HTTP_200_OK)
def add_pet(pet: Pet):
    """Add a new pet to the store"""
    from app.database import db
    pet_id = db.create_pet(pet.model_dump(exclude_unset=True))
    return db.get_pet(pet_id)


@router.put("", response_model=Pet)
def update_pet(pet: Pet):
    """Update an existing pet"""
    from app.database import db
    if not pet.id:
        raise HTTPException(status_code=400, detail="Invalid ID supplied")
    existing = db.get_pet(pet.id)
    if not existing:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.update_pet(pet.id, pet.model_dump(exclude_unset=True))
    return db.get_pet(pet.id)


@router.get("/findByStatus", response_model=List[Pet])
def find_pets_by_status(status: PetStatus = PetStatus.available):
    """Finds Pets by status"""
    from app.database import db
    return db.find_pets_by_status([status.value])


@router.get("/findByTags", response_model=List[Pet])
def find_pets_by_tags(tags: List[str]):
    """Finds Pets by tags"""
    from app.database import db
    return db.find_pets_by_tags(tags)


@router.get("/{petId}", response_model=Pet)
def get_pet_by_id(petId: int):
    """Find pet by ID"""
    from app.database import db
    pet = db.get_pet(petId)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.post("/{petId}")
def update_pet_with_form(
    petId: int,
    name: Optional[str] = Form(None),
    status: Optional[str] = Form(None)
):
    """Updates a pet in the store with form data"""
    from app.database import db
    pet = db.get_pet(petId)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    update_data = {
        "name": pet["name"],
        "photoUrls": pet["photoUrls"],
        "category": pet.get("category"),
        "tags": pet.get("tags"),
        "status": pet.get("status")
    }
    if name:
        update_data["name"] = name
    if status:
        update_data["status"] = status
    db.update_pet(petId, update_data)
    return db.get_pet(petId)


@router.delete("/{petId}")
def delete_pet(petId: int):
    """Deletes a pet"""
    from app.database import db
    if not db.delete_pet(petId):
        raise HTTPException(status_code=400, detail="Invalid pet value")
    return JSONResponse(content={"message": "Pet deleted"}, status_code=200)


@router.post("/{petId}/uploadImage", response_model=ApiResponse)
def upload_file(
    petId: int,
    additionalMetadata: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """uploads an image"""
    from app.database import db
    pet = db.get_pet(petId)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return ApiResponse(
        code=200,
        type="success",
        message=f"File uploaded successfully. Metadata: {additionalMetadata}"
    )
