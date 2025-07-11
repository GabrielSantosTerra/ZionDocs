from fastapi import APIRouter

router = APIRouter()

@router.get("/user")
def user():
    return "ZionDocs backend ativo - Rota de usuários"
