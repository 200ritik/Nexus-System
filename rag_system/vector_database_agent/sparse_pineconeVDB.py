import os
import logging

from dotenv import load_dotenv
from pinecone import Pinecone


load_dotenv()

PINECONE_SPARSE_INDEX_NAME = os.environ[
    "PINECONE_SPARSE_INDEX_NAME"
]

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Create Pinecone client
# --------------------------------------------------

def create_pinecone_client() -> Pinecone:
    """
    Establish the Pinecone connection.
    """

    api_key = os.environ["PINECONE_API_KEY"]

    client = Pinecone(
        api_key=api_key
    )

    logger.info(
        "Pinecone client created successfully."
    )

    return client


# --------------------------------------------------
# Get sparse Pinecone index
# --------------------------------------------------

def get_sparse_pinecone_index(
    client: Pinecone
):
    """
    Connect to the existing sparse Pinecone index.
    """

    index = client.Index(
        PINECONE_SPARSE_INDEX_NAME
    )

    logger.info(
        "Pinecone sparse index connected | index=%s",
        PINECONE_SPARSE_INDEX_NAME,
    )

    return index


# --------------------------------------------------
# Create chunk ID
# --------------------------------------------------

def create_chunk_id(
    document_id: str,
    chunk_index: int,
) -> str:

    return f"{document_id}_chunk_{chunk_index}"


# --------------------------------------------------
# Attach metadata
# --------------------------------------------------

def attach_metadata(
    file_name: str,
    document_id: str,
    page_number: int | None,
    chunk_id: str,
) -> dict:

    metadata = {
        "file_name": file_name,
        "document_id": document_id,
        "chunk_id": chunk_id,
    }

    if page_number is not None:
        metadata["page_number"] = page_number

    return metadata


# --------------------------------------------------
# Prepare sparse vector
# --------------------------------------------------

def prepare_sparse_vector(
    chunk: dict,
    sparse_vector: dict,
) -> dict:

    document_id = str(
        chunk["document_id"]
    )

    chunk_index = int(
        chunk["chunk_index"]
    )

    chunk_id = create_chunk_id(
        document_id=document_id,
        chunk_index=chunk_index,
    )

    page_number = None

    chunk_metadata = chunk.get(
        "metadata",
        {},
    )

    if isinstance(chunk_metadata, dict):

        page_number = (
            chunk_metadata.get("page_number")
            or chunk_metadata.get("page")
        )

    metadata = attach_metadata(
        file_name=chunk.get("file_name"),
        document_id=document_id,
        page_number=page_number,
        chunk_id=chunk_id,
    )

    sparse_vector_record = {
        "id": chunk_id,
        "sparse_values": sparse_vector,
        "metadata": metadata,
    }

    return sparse_vector_record


# --------------------------------------------------
# Upsert sparse vectors
# --------------------------------------------------

def upsert_sparse_vectors(
    index,
    sparse_chunks: list[dict],
) -> None:

    if not sparse_chunks:
        logger.warning(
            "No sparse chunks to upsert."
        )
        return

    logger.info(
        "Upserting sparse vectors to Pinecone | total_chunks=%d",
        len(sparse_chunks),
    )

    sparse_vectors = []

    for chunk in sparse_chunks:

        sparse_vector = chunk.get(
            "sparse_vector"
        )

        if sparse_vector is None:

            logger.warning(
                "Skipping chunk with no sparse vector | "
                "chunk_index=%s",
                chunk.get("chunk_index"),
            )

            continue

        vector = prepare_sparse_vector(
            chunk=chunk,
            sparse_vector=sparse_vector,
        )

        sparse_vectors.append(vector)

    if not sparse_vectors:

        logger.warning(
            "No valid sparse vectors to upsert."
        )

        return

    try:

        index.upsert(
            vectors=sparse_vectors
        )

        logger.info(
            "Sparse vectors upserted successfully | total=%d",
            len(sparse_vectors),
        )

    except Exception as error:

        logger.error(
            "Failed to upsert sparse vectors | error=%s",
            error,
            exc_info=True,
        )

        raise