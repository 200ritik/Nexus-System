import os
import logging
import tempfile
from pathlib import Path

import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
REGION_NAME = os.getenv("REGION_NAME")
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")

logger = logging.getLogger(__name__)


def file_fetching(
    user_id: str,
    document_id: str,
    object_key: str,
) -> str:
    """
    Download a PDF from S3 into a temporary local file.

    Returns:
        str: Path to the downloaded PDF.
    """

    if not BUCKET_NAME:
        raise ValueError("BUCKET_NAME is missing from .env")

    if not REGION_NAME:
        raise ValueError("REGION_NAME is missing from .env")

    if not object_key:
        raise ValueError("S3 object key is required")

    logger.info(
        "Fetching document_id=%s for user_id=%s",
        document_id,
        user_id,
    )

    # Use the configured credentials when supplied.
    client_kwargs = {"region_name": REGION_NAME}

    if ACCESS_KEY and SECRET_ACCESS_KEY:
        client_kwargs["aws_access_key_id"] = ACCESS_KEY
        client_kwargs["aws_secret_access_key"] = SECRET_ACCESS_KEY

    s3_client = boto3.client("s3", **client_kwargs)

    temp_path = None

    try:
        # Download to a temporary PDF file.
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            prefix=f"{document_id}_",
            delete=False,
        ) as temp_file:
            temp_path = temp_file.name

        s3_client.download_file(
            BUCKET_NAME,
            object_key,
            temp_path,
        )

        if not Path(temp_path).is_file() or Path(temp_path).stat().st_size == 0:
            raise ValueError("Downloaded PDF is missing or empty")

        logger.info(
            "Successfully downloaded document_id=%s (%d bytes)",
            document_id,
            Path(temp_path).stat().st_size,
        )

        return temp_path

    except (ClientError, Exception):
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        logger.exception(
            "Failed to download document_id=%s from S3",
            document_id,
        )
        raise