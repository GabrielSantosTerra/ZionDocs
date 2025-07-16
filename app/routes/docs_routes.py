from fastapi import APIRouter, UploadFile, Form, Depends, Query
from app.utils.s3_utils import upload_file_to_s3
from app.database.connection import get_db
from app.models.docs_models import Documento
from uuid import uuid4
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/upload")
async def upload_document(
    id_cliente: str = Form(...),
    tag: str = Form(...),
    file: UploadFile = Form(...),
    db: Session = Depends(get_db)
):
    uuid_str = str(uuid4())
    s3_key = f"{id_cliente}/{uuid_str}_{file.filename}"

    s3_url = upload_file_to_s3(file.file, s3_key, file.content_type)

    doc = Documento(
        uuid=uuid_str,
        id_cliente=id_cliente,
        tag=tag,
        s3_key=s3_key,
        url=s3_url
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {"id": doc.id, "uuid": doc.uuid, "url": doc.url}

@router.get("/search")
def buscar_documentos(
    id_cliente: str = Query(...),
    tag: str = Query(...),
    db: Session = Depends(get_db)
):
    documentos = (
        db.query(Documento)
        .filter(Documento.id_cliente.ilike(f"%{id_cliente}%"), Documento.tag.ilike(f"%{tag}%"))
        .order_by(Documento.created_at.desc())
        .all()
    )

    return [
        {
            "id": doc.id,
            "uuid": doc.uuid,
            "url": doc.url,
            "tag": doc.tag,
            "created_at": doc.created_at
        }
        for doc in documentos
    ]

