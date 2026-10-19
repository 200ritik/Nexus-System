from fastapi import APIRouter, Depends
from uuid import uuid4

from authentication.current_user import get_current_user_id

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/")
def upload_document(
    user_id: str = Depends(get_current_user_id),
):
    document_id = str(uuid4())

    return {
        "user_id": user_id,
        "document_id": document_id,
        "status": "pending",
    }
