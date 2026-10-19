
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from database.S3_BUCKET.connection import get_s3_client
from database.S3_BUCKET.S3_storage import file_s3_storage

logger = logging.getLogger(__name__)

FILE_PATH = "temp_uploades/blood_report.pdf"
BUCKET = os.getenv("BUCKET_NAME")
USER_ID = "test-user-123"  # Temporary ID for testing


def file_storage():
    logger.info("Storing file in S3 bucket")

    file_path = Path(FILE_PATH)

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not BUCKET:
        raise ValueError("BUCKET_NAME is missing from .env")

    result = file_s3_storage(
        uploaded_file=str(file_path),
        user_id=USER_ID,
        bucket_name=BUCKET,
    )

    s3_client = get_s3_client()

    s3_client.head_object(
        Bucket=BUCKET,
        Key=result["object_key"],
    )

    print("SUCCESS: File exists in S3!")
    print("Object key:", result["object_key"])

    return result


if __name__ == "__main__":
    file_storage()
