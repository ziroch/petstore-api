from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import pet, store, user


app = FastAPI(
    title="OpenAPI Petstore",
    description="This is a sample server Petstore server.",
    version="1.0.0",
    license_info={"name": "Apache-2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
    contact={"name": "API Support", "url": "https://github.com/agimenezpy-ucom/openapi-petstore"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pet.router)
app.include_router(store.router)
app.include_router(user.router)


@app.get("/", include_in_schema=False)
def root():
    return {"message": "PetStore API - Go to /docs for Swagger UI"}
