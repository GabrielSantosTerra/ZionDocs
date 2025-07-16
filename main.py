from fastapi import FastAPI
from app.routes import docs_routes as documentos
from app.routes import user_routes as usuarios

app = FastAPI()

app.include_router(usuarios.router, prefix="/users", tags=["Usuários"])
app.include_router(documentos.router, prefix="/documents", tags=["Documentos"])

@app.get("/")
def read_root():
    return {"message": "ZionDocs API ativa"}
