from fastapi import UploadFile
from pydantic import BaseModel

class DocumentUploadRequest(BaseModel):
    id_cliente: int
    tag: str
