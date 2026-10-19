import logging
import os

from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

logger = logging.getLogger(__name__)

PINECONE_DENSE_INDEX_NAME = os.environ["PINECONE_DENSE_INDEX_NAME"]


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

    logger.info("Pinecone client created successfully.")

    return client


# --------------------------------------------------
# Get Pinecone index
# --------------------------------------------------

def get_pinecone_index(client: Pinecone):
    """
    Get the Pinecone index used by the application.
    """

    index = client.Index(
        PINECONE_DENSE_INDEX_NAME
    )

    logger.info(
        "Pinecone index connected | index=%s",
        PINECONE_DENSE_INDEX_NAME,
    )

    return index


# --------------------------------------------------
# Create chunk ID
# --------------------------------------------------

def create_chunk_id(
    document_id: str,
    chunk_index: int,
) -> str:
    """
    Create a unique ID for a document chunk.
    """

    chunk_id = f"{document_id}_chunk_{chunk_index}"

    return chunk_id


# --------------------------------------------------
# Attach metadata
# --------------------------------------------------

def attach_metadata(
    file_name: str,
    document_id: str,
    page_number: int | None,
    chunk_id: str,
) -> dict:
    """
    Attach metadata to a Pinecone vector.
    """

    vector_metadata = {
        "file_name": file_name,
        "document_id": document_id,
        "chunk_id": chunk_id,
    }

    if page_number is not None:
        vector_metadata["page_number"] = page_number

    return vector_metadata


# --------------------------------------------------
# Prepare vector
# --------------------------------------------------

def prepare_vector(
    chunk: dict,
    embedding,
) -> dict:
    """
    Prepare one Pinecone vector record.
    """

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
        {}
    )

    if isinstance(chunk_metadata, dict):

        page_number = (
            chunk_metadata.get("page_number")
            or chunk_metadata.get("page")
        )

    metadata = attach_metadata(
        file_name=chunk["file_name"],
        document_id=document_id,
        page_number=page_number,
        chunk_id=chunk_id,
    )

    vector = {
        "id": chunk_id,
        "values": (
            embedding.tolist()
            if hasattr(embedding, "tolist")
            else embedding
        ),
        "metadata": metadata,
    }

    return vector


# --------------------------------------------------
# Store vectors in Pinecone
# --------------------------------------------------

def upsert_vectors(
    index,
    embedded_chunks: list[dict],
) -> None:
    """
    Store embedded chunks in Pinecone.
    """

    if not embedded_chunks:
        logger.warning(
            "No embedded chunks supplied."
        )
        return

    vectors = []

    for chunk in embedded_chunks:

        embedding = chunk.get(
            "embedding"
        )

        if embedding is None:

            logger.warning(
                "Skipping chunk without embedding | "
                "chunk_index=%s",
                chunk.get("chunk_index"),
            )

            continue

        try:

            vector = prepare_vector(
                chunk=chunk,
                embedding=embedding,
            )

            vectors.append(vector)

        except Exception as error:

            logger.error(
                "Failed to prepare vector | "
                "chunk_index=%s | error=%s",
                chunk.get("chunk_index"),
                error,
                exc_info=True,
            )

            raise

    if not vectors:

        logger.warning(
            "No valid vectors to upsert."
        )

        return

    try:

        index.upsert(
            vectors=vectors
        )

        logger.info(
            "Vectors successfully stored in Pinecone | "
            "total=%d",
            len(vectors),
        )

    except Exception as error:

        logger.error(
            "Pinecone vector upsert failed | "
            "error=%s",
            error,
            exc_info=True,
        )

        raise