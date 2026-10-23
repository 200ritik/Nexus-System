import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from botocore.exceptions import ClientError

from rag_system.ingestion_agent.ingestion_layer import INGESTION_AGENT

# Load the project's root .env file
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_ingestion():
    user_id = "test-user-123"
    document_id = "0bebe8b7-7272-4ad0-9dd7-601b3f3008e0"
    file_name = "blood_report.pdf"

    # Match the object key of the PDF already uploaded to S3.
    object_key = (
        f"users/{user_id}/documents/{document_id}/{file_name}"
    )

    # Verify required configuration without printing secrets.
    required_vars = [
        "ACCESS_KEY",
        "SECRET_ACCESS_KEY",
        "REGION_NAME",
        "BUCKET_NAME",
    ]

    missing = [
        name for name in required_vars
        if not os.getenv(name)
    ]

    assert not missing, f"Missing .env variables: {missing}"

    assert os.getenv("BUCKET_NAME") == "nexus-medical-storage"

    try:
        result = INGESTION_AGENT(
            user_id=user_id,
            document_id=document_id,
            object_key=object_key,
            file_name=file_name,
        )

        assert result["status"] == "completed"
        assert result["document_id"] == document_id
        assert result["chunk_count"] > 0

        logger.info("Ingestion test passed: %s", result)

    except ClientError:
        logger.exception(
            "AWS request failed. Check AWS credentials, region, "
            "bucket permissions, and the S3 object key."
        )
        raise


if __name__ == "__main__":
    test_ingestion()
