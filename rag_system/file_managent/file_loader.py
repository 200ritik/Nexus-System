
"""
Load a file from S3 using LangChain's S3FileLoader.
"""

import os
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders import S3FileLoader

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
REGION_NAME = os.getenv("REGION_NAME")

logger = logging.getLogger(__name__)


def file_fetching(user_id: str, document_id: str, object_key: str):
    """
    Fetch a document from S3 for the ingestion layer.

    user_id: Authenticated user's ID.
    document_id: Document ID retrieved from PostgreSQL.
    object_key: S3 key retrieved from PostgreSQL.
    """

    if not BUCKET_NAME:
        raise ValueError("BUCKET_NAME is missing from .env")

    if not object_key:
        raise ValueError("S3 object key is required")

    logger.info(
        "Loading document_id=%s for user_id=%s",
        document_id,
        user_id,
    )

    loader = S3FileLoader(
        bucket=BUCKET_NAME,
        key=object_key,
        region_name=REGION_NAME,
    )

    document = loader.load()

    logger.info("Successfully loaded %s document(s)", len(document))

    return document
