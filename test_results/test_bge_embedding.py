from pathlib import Path

from rag_system.parser_agent.doc_parsing import file_parsing
from rag_system.chunking_agent.Hybrid_chunking import chunks_documents
from rag_system.embedding_agent.bge_embedding import file_embed


# ============================================================
# TEST FILE
# ============================================================

TEST_FILE = Path(r"temp_uploades/blood_report.pdf")


# ============================================================
# TEST BGE-M3 EMBEDDING
# ============================================================

def test_bge_embedding():

    print("\n" + "=" * 70)
    print("TESTING DOCLING + HYBRID CHUNKING + BGE-M3")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Parse document
    # --------------------------------------------------------

    parsed_files = file_parsing(
        [str(TEST_FILE)]
    )

    assert parsed_files, "Parsing returned no documents."

    print(
        f"\nParsed documents: {len(parsed_files)}"
    )

    # --------------------------------------------------------
    # 2. Create chunks
    # --------------------------------------------------------

    all_chunks = chunks_documents(
        parsed_files
    )

    assert all_chunks, "Chunking returned no chunks."

    print(
        f"Total chunks: {len(all_chunks)}"
    )

    # --------------------------------------------------------
    # 3. Generate BGE-M3 embeddings
    # --------------------------------------------------------

    embedded_chunks = file_embed(
        all_chunks
    )

    assert embedded_chunks, (
        "Embedding returned no results."
    )

    print(
        f"Embedded chunks: {len(embedded_chunks)}"
    )

    # --------------------------------------------------------
    # 4. Validate embeddings
    # --------------------------------------------------------

    for chunk in embedded_chunks:

        assert "embedding" in chunk

        embedding = chunk["embedding"]

        assert embedding is not None

        print(
            f"\nChunk index: {chunk['chunk_index']}"
        )

        print(
            f"Text: {chunk['text'][:100]}..."
        )

        print(
            f"Embedding type: {type(embedding)}"
        )

        try:
            print(
                f"Embedding dimensions: {len(embedding)}"
            )
        except TypeError:
            print(
                "Could not determine embedding length."
            )

    # --------------------------------------------------------
    # 5. Verify first embedding
    # --------------------------------------------------------

    first_embedding = embedded_chunks[0]["embedding"]

    assert first_embedding is not None

    print("\n" + "=" * 70)
    print("FIRST EMBEDDING")
    print("=" * 70)

    print(
        f"Type: {type(first_embedding)}"
    )

    print(
        f"Dimensions: {len(first_embedding)}"
    )

    print(
        f"First 10 values: {first_embedding[:10]}"
    )

    # --------------------------------------------------------
    # 6. Final result
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("BGE-M3 EMBEDDING TEST PASSED")
    print("=" * 70)


# ============================================================
# RUN TEST
# ============================================================

if __name__ == "__main__":
    test_bge_embedding()