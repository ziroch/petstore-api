# PetStore API - FastAPI

Implementación de una API RESTful basada en OpenAPI PetStore usando FastAPI y SQLite.

## Requisitos
- Python 3.10+

## Instalación
pip install -r requirements.txt

## Ejecución
uvicorn app.main:app --reload

## Documentación
Swagger UI: http://localhost:8000/docs  
ReDoc: http://localhost:8000/redoc

## Endpoints principales
- POST /pet
- GET /pet/{id}
- GET /pet
