import logging

from database.postgresql.connection import get_postgres_connection

logger = logging.getLogger(__name__)


def save_document_metadata(
    document_id: str,
    user_id: str,
    file_name: str,
    s3_object_key: str,
    file_hash: str,
) -> None:

    connection = None
    cursor = None

    try:
        connection = get_postgres_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO documents (
                document_id,
                user_id,
                file_name,
                s3_object_key,
                file_hash,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        cursor.execute(
            query,
            (
                document_id,
                user_id,
                file_name,
                s3_object_key,
                file_hash,
                "uploaded",
            ),
        )

        connection.commit()

        logger.info(
            "Document metadata saved | document_id=%s | file=%s",
            document_id,
            file_name,
        )

    except Exception:
        if connection:
            connection.rollback()

        logger.exception(
            "Failed to save document metadata | document_id=%s",
            document_id,
        )
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()