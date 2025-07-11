from fastapi import APIRouter

router = APIRouter()

@router.get("/docs")
def docs():
    return "ZionDocs backend ativo - Rota de documentos"
