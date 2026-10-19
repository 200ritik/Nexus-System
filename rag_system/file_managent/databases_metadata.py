
from datetime import datetime, timezone


# Custom metadata for the S3 object.
def s3_storage_metadata(
    user_id: str,
    document_id: str,
    file_name: str,
    object_key: str
) -> dict:
    return {
        "user_id": str(user_id),
        "document_id": str(document_id),
        "file_name": file_name,
        "object" : object_key
    }


# Metadata for the PostgreSQL document table.
def postgre_document_table_metadata(
    user_id: str,
    document_id: str,
    file_name: str,
    s3_object_key: str,
    status: str = "pending",
    created_at: datetime | None = None,
    file_size_byte: int | None = None,
    mime_type: str = "application/pdf",
    error_message: str | None = None,
    processed_at: datetime | None = None,
    expires_at: datetime | None = None,
) -> dict:
    return {
        "user_id": str(user_id),
        "document_id": str(document_id),
        "file_name": file_name,
        "s3_object_key": s3_object_key,
        "status": status,
        "created_at": created_at or datetime.now(timezone.utc),
        "file_size_byte": file_size_byte,
        "mime_type": mime_type,
        "error_message": error_message,
        "processed_at": processed_at,
        "expires_at": expires_at,
    }

    
    