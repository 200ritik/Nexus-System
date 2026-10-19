import logging

from pinecone_text.sparse import BM25Encoder

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Create sparse encoder
# --------------------------------------------------

def create_sparse_encoder() -> BM25Encoder:
    logger.info("Creating BM25 sparse encoder.")

    encoder = BM25Encoder()

    logger.info("BM25 sparse encoder created successfully.")

    return encoder


# --------------------------------------------------
# Fit encoder on all chunk text
# --------------------------------------------------

def fit_sparse_encoder(
    encoder: BM25Encoder,
    all_chunks: list[dict],
) -> BM25Encoder:

    if not all_chunks:
        raise ValueError("No chunks supplied.")

    documents = []

    for chunk in all_chunks:

        text = chunk.get("text")

        if not text or not text.strip():
            logger.warning(
                "Skipping chunk without text | chunk_index=%s",
                chunk.get("chunk_index"),
            )
            continue

        documents.append(text)

    if not documents:
        raise ValueError(
            "No valid chunk text found."
        )

    logger.info(
        "Fitting BM25 encoder | documents=%d",
        len(documents),
    )

    encoder.fit(documents)

    logger.info(
        "BM25 encoder fitted successfully."
    )

    return encoder


# --------------------------------------------------
# Encode one chunk
# --------------------------------------------------

def encoding_text(
    encoder: BM25Encoder,
    text: str,
) -> dict:

    if not text or not text.strip():
        raise ValueError(
            "No text supplied for encoding."
        )

    return encoder.encode_documents(
        text
    )


# --------------------------------------------------
# Encode all chunks
# --------------------------------------------------

def chunks_encoder(
    all_chunks: list[dict],
) -> list[dict]:

    if not all_chunks:
        logger.warning(
            "No chunks supplied for sparse encoding."
        )
        return []

    logger.info(
        "Sparse encoding started | chunks=%d",
        len(all_chunks),
    )

    # Create ONE encoder
    encoder = create_sparse_encoder()

    # Fit it on the COMPLETE chunk corpus
    fit_sparse_encoder(
        encoder=encoder,
        all_chunks=all_chunks,
    )

    sparse_chunks = []

    for chunk in all_chunks:

        text = chunk.get("text")

        if not text or not text.strip():
            logger.warning(
                "Skipping empty chunk | chunk_index=%s",
                chunk.get("chunk_index"),
            )
            continue

        try:

            sparse_vector = encoding_text(
                encoder=encoder,
                text=text,
            )

            sparse_chunks.append(
                {
                    "chunk_index": chunk.get(
                        "chunk_index"
                    ),
                    "document_id": chunk.get(
                        "document_id"
                    ),
                    "file_name": chunk.get(
                        "file_name"
                    ),
                    "text": text,
                    "sparse_vector": sparse_vector,
                    "metadata": chunk.get(
                        "metadata",
                        {},
                    ),
                }
            )

        except Exception as error:

            logger.error(
                "Sparse encoding failed | "
                "chunk_index=%s | error=%s",
                chunk.get("chunk_index"),
                error,
                exc_info=True,
            )

            raise

    logger.info(
        "Sparse encoding completed | "
        "successful=%d",
        len(sparse_chunks),
    )

    return sparse_chunks