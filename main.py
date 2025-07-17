from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import docs_routes as documentos
from app.routes import user_routes as usuarios

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://docrh-615cf.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router, prefix="/users", tags=["Usuários"])
app.include_router(documentos.router, prefix="/documents", tags=["Documentos"])

@app.get("/")
def read_root():
    return {"message": "ZionDocs API ativa"}
