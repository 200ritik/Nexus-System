import logging

from rag_system.vector_database_agent.pineconeVDB import (
    create_pinecone_client,
    get_pinecone_index,
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Connect to dense Pinecone index
# --------------------------------------------------

def create_dense_index():

    client = create_pinecone_client()

    index = get_pinecone_index(
        client
    )

    logger.info(
        "Dense Pinecone index connected."
    )

    return index


# --------------------------------------------------
# Search dense index
# --------------------------------------------------

def dense_index(
    index,
    dense_query_vector,
    top_k: int = 10,
) -> list[dict]:

    if dense_query_vector is None:
        raise ValueError(
            "Dense query vector cannot be None."
        )

    try:

        logger.info(
            "Dense search started."
        )

        response = index.query(
            vector=dense_query_vector,
            top_k=top_k,
            include_metadata=True,
        )

        dense_results = []

        for rank, match in enumerate(
            response.matches,
            start=1,
        ):

            dense_results.append(
                {
                    "chunk_id": match.id,
                    "score": match.score,
                    "metadata": match.metadata,
                    "rank": rank,
                }
            )

        logger.info(
            "Dense search completed | results=%d",
            len(dense_results),
        )

        return dense_results

    except Exception as error:

        logger.error(
            "Dense search failed | error=%s",
            error,
            exc_info=True,
        )

        raise