
import logging
import uuid
from pathlib import Path

from database.S3_BUCKET.connection import get_s3_client
from rag_system.file_managent.databases_metadata import (
    s3_storage_metadata,
)
from rag_system.file_managent.file_upload import file_checking

logger = logging.getLogger(__name__)


def file_s3_storage(
    uploaded_file: str,
    user_id: str,
    bucket_name: str,
) -> dict:
    """Validate and upload one supported file to S3."""

    file_path = Path(uploaded_file)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"File does not exist: {file_path}"
        )

    logger.info("Validating file: %s", file_path.name)

    # 1. Validate the file.
    validated_file = file_checking(str(file_path))

    # 2. Generate a unique document ID.
    document_id = str(uuid.uuid4())

    # 3. Generate the S3 object key.
    object_key = (
        f"users/{user_id}/documents/"
        f"{document_id}/{validated_file['file_name']}"
    )

    # 4. Prepare metadata.
    metadata = s3_storage_metadata(
        user_id=user_id,
        document_id=document_id,
        file_name=validated_file["file_name"],
        object_key=object_key,
    )

    # 5. Upload to S3.
    s3_client = get_s3_client()

    try:
        s3_client.upload_file(
            str(file_path),
            bucket_name,
            object_key,
            ExtraArgs={
                "Metadata": {
                    "user_id": str(user_id),
                    "document_id": str(document_id),
                    "file_name": validated_file["file_name"],
                },
                "ContentType": validated_file.get(
                    "mime_type",
                    "application/octet-stream",
                ),
            },
        )

        logger.info(
            "S3 upload successful: document_id=%s",
            document_id,
        )

        return {
            "user_id": str(user_id),
            "document_id": document_id,
            "file_name": validated_file["file_name"],
            "object_key": object_key,
            "mime_type": validated_file.get("mime_type"),
            "status": "pending",
        }

    except Exception:
        logger.exception(
            "S3 upload failed for document_id=%s",
            document_id,
        )
        raise
