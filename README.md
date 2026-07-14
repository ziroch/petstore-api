PetStore API - FastAPI Implementation

Implementación de la API RESTful PetStore usando FastAPI + SQLite en memoria, respetando la especificación OpenAPI del repositorio [openapi-petstore](https://github.com/agimenezpy-ucom/openapi-petstore).

---

Requisitos

- Python 3.10+
- pip

---

Instalación y Ejecución

1. Clonar / descargar el proyecto


cd petstore-api


2. Crear entorno virtual (recomendado)


python -m venv venv

source venv/bin/activate


3. Instalar dependencias


pip install -r requirements.txt


4. Ejecutar el servidor


uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


5. Acceder a la documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

---

Endpoints Principales

Pet (`/pet`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/pet` | Add a new pet |
| PUT | `/pet` | Update an existing pet |
| GET | `/pet/findByStatus` | Find pets by status |
| GET | `/pet/findByTags` | Find pets by tags |
| GET | `/pet/{petId}` | Get pet by ID |
| POST | `/pet/{petId}` | Update pet with form data |
| DELETE | `/pet/{petId}` | Delete a pet |
| POST | `/pet/{petId}/uploadImage` | Upload an image |

Store (`/store`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/store/inventory` | Returns pet inventories by status |
| POST | `/store/order` | Place an order for a pet |
| GET | `/store/order/{orderId}` | Find purchase order by ID |
| DELETE | `/store/order/{orderId}` | Delete purchase order by ID |

User (`/user`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/user` | Create user |
| POST | `/user/createWithArray` | Create users with array |
| POST | `/user/createWithList` | Create users with list |
| GET | `/user/login` | Logs user into the system |
| GET | `/user/logout` | Logs out current session |
| GET | `/user/{username}` | Get user by name |
| PUT | `/user/{username}` | Update user |
| DELETE | `/user/{username}` | Delete user |

---

Pruebas Rápidas (cURL)

Crear una mascota

curl -X POST "http://localhost:8000/pet"   -H "Content-Type: application/json"   -d '{
    "name": "doggie",
    "photoUrls": ["https://example.com/dog.jpg"],
    "status": "available",
    "category": {"id": 1, "name": "Dogs"},
    "tags": [{"id": 1, "name": "friendly"}]
  }'


 Obtener mascota por ID

curl "http://localhost:8000/pet/1"


 Buscar por status

curl "http://localhost:8000/pet/findByStatus?status=available"


 Crear orden

curl -X POST "http://localhost:8000/store/order"   -H "Content-Type: application/json"   -d '{"petId": 1, "quantity": 2, "status": "placed"}'


 Ver inventario

curl "http://localhost:8000/store/inventory"


 Crear usuario

curl -X POST "http://localhost:8000/user"   -H "Content-Type: application/json"   -d '{"username": "john_doe", "firstName": "John", "email": "john@example.com", "password": "secret"}'


 Login

curl "http://localhost:8000/user/login?username=john_doe&password=secret"


---

Arquitectura


app/
├── main.py           FastAPI app + routers
├── models.py         Pydantic models (OpenAPI schemas)
├── database.py       SQLite in-memory layer
└── routers/
    ├── pet.py        /pet endpoints
    ├── store.py      /store endpoints
    └── user.py       /user endpoints


---

Notas

- La base de datos es SQLite en memoria; los datos se pierden al reiniciar el servidor.
- Las validaciones de Pydantic respetan los tipos, enums y campos requeridos de la especificación OpenAPI.

---

Referencias

- [Especificación OpenAPI PetStore](https://petstore3.swagger.io/)
- [Repositorio OpenAPI Generator](https://github.com/OpenAPITools/openapi-petstore)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
