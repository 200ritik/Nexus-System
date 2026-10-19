import logging

from rag_system.parser_agent.doc_parsing import file_parsing
from rag_system.chunking_agent.Hybrid_chunking import chunks_documents
from rag_system.embedding_agent.sparse_embedding import chunks_encoder


# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)


# --------------------------------------------------
# Test file
# --------------------------------------------------

TEST_FILE = (r"temp_uploades/blood_report.pdf")


# --------------------------------------------------
# Sparse embedding test
# --------------------------------------------------

def test_sparse_embedding():

    print("\n" + "=" * 60)
    print("SPARSE EMBEDDING TEST")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Parse document
    # --------------------------------------------------

    parsed_files = file_parsing(
        [TEST_FILE]
    )

    print(
        f"\nParsed documents: {len(parsed_files)}"
    )

    assert parsed_files, (
        "Document parsing failed."
    )

    # --------------------------------------------------
    # 2. Chunk document
    # --------------------------------------------------

    all_chunks = chunks_documents(
        parsed_files
    )

    print(
        f"Total chunks: {len(all_chunks)}"
    )

    assert all_chunks, (
        "Chunking failed."
    )

    # --------------------------------------------------
    # 3. Create sparse vectors
    # --------------------------------------------------

    sparse_chunks = chunks_encoder(
        all_chunks
    )

    print(
        f"Sparse encoded chunks: "
        f"{len(sparse_chunks)}"
    )

    assert sparse_chunks, (
        "Sparse encoding failed."
    )

    # --------------------------------------------------
    # 4. Validate sparse vectors
    # --------------------------------------------------

    for chunk in sparse_chunks:

        sparse_vector = chunk.get(
            "sparse_vector"
        )

        assert sparse_vector is not None, (
            "Sparse vector is missing."
        )

        assert isinstance(
            sparse_vector,
            dict,
        ), (
            "Sparse vector should be a dictionary."
        )

        assert "indices" in sparse_vector, (
            "Sparse vector has no indices."
        )

        assert "values" in sparse_vector, (
            "Sparse vector has no values."
        )

        assert len(
            sparse_vector["indices"]
        ) == len(
            sparse_vector["values"]
        ), (
            "Sparse indices and values "
            "length mismatch."
        )

    # --------------------------------------------------
    # 5. Display first sparse vector
    # --------------------------------------------------

    first_chunk = sparse_chunks[0]

    first_vector = first_chunk[
        "sparse_vector"
    ]

    print("\nFirst sparse vector:")

    print(
        f"Chunk index: "
        f"{first_chunk.get('chunk_index')}"
    )

    print(
        f"Document ID: "
        f"{first_chunk.get('document_id')}"
    )

    print(
        f"Non-zero indices: "
        f"{len(first_vector['indices'])}"
    )

    print(
        f"Values: "
        f"{len(first_vector['values'])}"
    )

    print(
        f"First 10 indices: "
        f"{first_vector['indices'][:10]}"
    )

    print(
        f"First 10 values: "
        f"{first_vector['values'][:10]}"
    )

    # --------------------------------------------------
    # 6. Final validation
    # --------------------------------------------------

    assert len(sparse_chunks) <= len(
        all_chunks
    )

    print("\n" + "=" * 60)
    print("SPARSE EMBEDDING TEST PASSED")
    print("=" * 60)


# --------------------------------------------------
# Run test
# --------------------------------------------------

if __name__ == "__main__":
    test_sparse_embedding()