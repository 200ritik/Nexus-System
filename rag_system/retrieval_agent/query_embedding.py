import logging
from rag_system.embedding_agent.bge_embedding import embedding_model, embed_text
from rag_system.embedding_agent.sparse_embedding import encoding_text, create_sparse_encoder

logger = logging.getLogger(__name__)

client = embedding_model()
encoder = create_sparse_encoder()

def dense_query_embedding(query:str)-> list:
    """embed the query and generate the dense vectors

    Args:
        query (str): users query

    Returns:
        list: return list of dense vector useing the bge-m3 model
    """
    
    try:
        logger.info("Generating dense embedding for the query...")

        dense_query_vector = embed_text(
            text=query,
            client=client
        )
        return dense_query_vector
    except Exception as e:
        logger.error(f"Error generating dense embedding: {e}")
        raise
    
def sparse_query_embedding(query:str)-> list:
    """generate the sparse embedding for the query using the sparse encoder

    Args:
        query (str): users query

    Returns:
        list: sparse matrix for the query
    """
    
    try:
        logger.info("Generating sparse embedding for the query...")

        sparse_query_vector = encoding_text(
            encoder=encoder,
            text=query
        )
        return sparse_query_vector
    except Exception as e:
        logger.error(f"Error generating sparse embedding: {e}")
        raise
    