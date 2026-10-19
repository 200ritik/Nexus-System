import logging

from rag_system.vector_database_agent.sparse_pineconeVDB import (
    create_pinecone_client,
    get_sparse_pinecone_index,
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Connect to sparse Pinecone index
# --------------------------------------------------

def create_sparse_index():

    client = create_pinecone_client()

    index = get_sparse_pinecone_index(
        client
    )

    logger.info(
        "Sparse Pinecone index connected."
    )

    return index


# --------------------------------------------------
# Search sparse index
# --------------------------------------------------

def sparse_index(
    index,
    sparse_query_vector,
    top_k: int = 10,
) -> list[dict]:

    if sparse_query_vector is None:
        raise ValueError(
            "Sparse query vector cannot be None."
        )

    try:

        logger.info(
            "Sparse search started."
        )

        response = index.query(
            sparse_vector=sparse_query_vector,
            top_k=top_k,
            include_metadata=True,
        )

        sparse_results = []
    
        for rank, match in enumerate(
            response.matches,
            start=1,
        ):

            sparse_results.append(
                {
                    "chunk_id": match.id,
                    "score": match.score,
                    "metadata": match.metadata,
                    "rank": rank,
                }
            )

        logger.info(
            "Sparse search completed | results=%d",
            len(sparse_results),
        )

        return sparse_results

    except Exception as error:

        logger.error(
            "Sparse search failed | error=%s",
            error,
            exc_info=True,
        )

        raise