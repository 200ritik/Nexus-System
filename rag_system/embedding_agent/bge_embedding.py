import logging
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

MODEL = "BAAI/bge-m3"

logger = logging.getLogger(__name__)

_model = None


# ============================================================
# LOAD LOCAL EMBEDDING MODEL
# ============================================================

def embedding_model() -> SentenceTransformer:
    """
    Load BGE-M3 locally.

    The model is loaded only once and reused for subsequent
    embedding requests.
    """
    global _model

    if _model is None:
        logger.info("Loading local embedding model: %s", MODEL)
        _model = SentenceTransformer(MODEL)
        logger.info("Local embedding model loaded successfully")

    return _model


# ============================================================
# EMBED SINGLE TEXT
# ============================================================

def embed_text(
    text: str,
    client: SentenceTransformer,
) -> list[float]:
    """
    Generate a normalized BGE-M3 dense embedding for one text.
    """

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    try:
        embedding = client.encode(
            text.strip(),
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        return np.asarray(
            embedding,
            dtype=np.float32,
        ).tolist()

    except Exception:
        logger.exception("Text embedding failed")
        raise


# ============================================================
# EMBED ALL CHUNKS
# ============================================================

def file_embed(
    all_chunks: list[dict],
) -> list[dict]:
    """
    Generate local BGE-M3 dense embeddings for document chunks.

    Original chunk metadata and text are preserved.
    """

    if not all_chunks:
        logger.warning("No chunks received for embedding.")
        return []

    client = embedding_model()
    embedded_chunks = []

    logger.info(
        "Embedding started | total_chunks=%d | model=%s",
        len(all_chunks),
        MODEL,
    )

    for chunk in all_chunks:
        chunk_index = chunk.get("chunk_index")
        text = chunk.get("text")

        if not isinstance(text, str) or not text.strip():
            logger.warning(
                "Skipping empty chunk | chunk_index=%s",
                chunk_index,
            )
            continue

        logger.info(
            "Embedding chunk | chunk_index=%s",
            chunk_index,
        )

        embedding = embed_text(
            text=text,
            client=client,
        )

        if len(embedding) != 1024:
            raise ValueError(
                f"Expected 1024-dimensional BGE-M3 embedding, "
                f"received {len(embedding)} dimensions."
            )

        embedded_chunks.append({
            **chunk,
            "embedding": embedding,
        })

    logger.info(
        "Embedding completed | successful=%d | skipped=%d",
        len(embedded_chunks),
        len(all_chunks) - len(embedded_chunks),
    )

    return embedded_chunks
