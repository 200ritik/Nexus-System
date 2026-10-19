from rag_system.parser_agent.doc_parsing import file_parsing
from rag_system.chunking_agent.Hybrid_chunking import chunks_documents
from rag_system.embedding_agent.bge_embedding import file_embed

from rag_system.vector_database_agent.pineconeVDB import (
    create_pinecone_client,
    get_pinecone_index,
    upsert_vectors,
)


TEST_FILE = (r"temp_uploades/blood_report.pdf")


def main():

    # ----------------------------------------------
    # 1. Parse document
    # ----------------------------------------------

    parsed_files = file_parsing(
        [TEST_FILE]
    )

    print(
        f"Parsed documents: {len(parsed_files)}"
    )

    if not parsed_files:
        raise RuntimeError(
            "Document parsing failed."
        )


    # ----------------------------------------------
    # 2. Chunk document
    # ----------------------------------------------

    all_chunks = chunks_documents(
        parsed_files
    )

    print(
        f"Total chunks: {len(all_chunks)}"
    )

    if not all_chunks:
        raise RuntimeError(
            "Chunking failed."
        )


    # ----------------------------------------------
    # 3. Generate embeddings
    # ----------------------------------------------

    embedded_chunks = file_embed(
        all_chunks
    )

    print(
        f"Embedded chunks: {len(embedded_chunks)}"
    )

    if not embedded_chunks:
        raise RuntimeError(
            "Embedding failed."
        )


    # ----------------------------------------------
    # 4. Create Pinecone client
    # ----------------------------------------------

    client = create_pinecone_client()

    print(
        "Pinecone client created successfully."
    )


    # ----------------------------------------------
    # 5. Connect to Pinecone index
    # ----------------------------------------------

    index = get_pinecone_index(
        client
    )

    print(
        "Pinecone index connected successfully."
    )


    # ----------------------------------------------
    # 6. Upsert vectors
    # ----------------------------------------------

    upsert_vectors(
        index=index,
        embedded_chunks=embedded_chunks,
    )

    print(
        "Vectors successfully stored in Pinecone."
    )


    # ----------------------------------------------
    # 7. Check index statistics
    # ----------------------------------------------

    stats = index.describe_index_stats()

    print("\nPINECONE INDEX STATS")
    print(stats)

    print(
        "\nPINECONE STORAGE TEST PASSED"
    )


if __name__ == "__main__":
    main()