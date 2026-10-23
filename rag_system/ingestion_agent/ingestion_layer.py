
# ingestion layer
import logging
# import logfire

# ingestion_layer packages ========================================

from rag_system.file_managent.file_loader import file_fetching
from rag_system.parser_agent.doc_parsing import file_parsing
from rag_system.chunking_agent.Hybrid_chunking import chunks_documents
from rag_system.embedding_agent.bge_embedding import file_embed
from rag_system.embedding_agent.sparse_embedding import chunks_encoder

from rag_system.vector_database_agent.pineconeVDB import (
    create_pinecone_client,
    get_pinecone_index,
    upsert_vectors,
)

from rag_system.vector_database_agent.sparse_pineconeVDB import (
    create_pinecone_client as create_sparse_pinecone_client,
    get_sparse_pinecone_index,
    upsert_sparse_vectors,
)

# observability layer =============================================

logger = logging.getLogger(__name__)
# logfire.configure()

# ========================= INGESTION LAYER =======================

def INGESTION_AGENT(
    user_id: str,
    document_id: str,
    object_key: str,
    file_name: str,
) -> dict:

    logger.info(
        "Starting ingestion | document_id=%s",
        document_id,
    )

    try:
        # ===================== STEP 1: FILE FETCHING ==============

        document = file_fetching(
            user_id=user_id,
            document_id=document_id,
            object_key=object_key,
        )

        # ===================== STEP 2: FILE PARSING ===============

        parsed_file = file_parsing(document)

        # ===================== STEP 3: HYBRID CHUNKING ============

        parsed_files = [
            {
                "user_id": user_id,
                "document_id": document_id,
                "file_name": file_name,
                "document": parsed_file,
            }
        ]

        all_chunks = chunks_documents(parsed_files)

        if not all_chunks:
            raise ValueError(
                "No chunks were generated from the document."
            )

        # ===================== STEP 4: DENSE VECTORS ==============

        embedded_chunks = file_embed(all_chunks)

        if not embedded_chunks:
            raise ValueError(
                "No dense embeddings were generated."
            )

        # ===================== STEP 5: SPARSE VECTORS =============

        sparse_chunks = chunks_encoder(all_chunks)

        if not sparse_chunks:
            raise ValueError(
                "No sparse vectors were generated."
            )

        # ===================== STEP 6: DENSE PINECONE =============

        dense_client = create_pinecone_client()
        dense_index = get_pinecone_index(dense_client)

        upsert_vectors(
            index=dense_index,
            embedded_chunks=embedded_chunks,
        )

        # ===================== STEP 7: SPARSE PINECONE ============

        sparse_client = create_sparse_pinecone_client()
        sparse_index = get_sparse_pinecone_index(
            sparse_client
        )

        upsert_sparse_vectors(
            index=sparse_index,
            sparse_chunks=sparse_chunks,
        )

        # ===================== STEP 8: SUCCESS ====================

        logger.info(
            "Ingestion completed | document_id=%s | chunks=%d",
            document_id,
            len(all_chunks),
        )

        return {
            "user_id": user_id,
            "document_id": document_id,
            "status": "completed",
            "chunk_count": len(all_chunks),
        }

    except Exception:
        logger.exception(
            "Ingestion failed | document_id=%s",
            document_id,
        )
        raise
