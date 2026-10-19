from pathlib import Path

from rag_system.parser_agent.doc_parsing import file_parsing
from rag_system.chunking_agent.Hybrid_chunking import chunks_documents


# ============================================================
# TEST FILE
# ============================================================

TEST_FILE = Path(r"temp_uploades/blood_report.pdf")


# ============================================================
# TEST
# ============================================================

def test_hybrid_chunking():

    print("\n" + "=" * 70)
    print("TESTING DOCLING + HYBRID CHUNKING")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Parse document using your actual parser
    # --------------------------------------------------------

    parsed_files = file_parsing(
        [str(TEST_FILE)]
    )

    assert parsed_files, "Parsing returned no documents."

    print(f"\nParsed documents: {len(parsed_files)}")

    # --------------------------------------------------------
    # 2. Pass parser output directly to HybridChunker
    # --------------------------------------------------------

    chunks = chunks_documents(
        parsed_files
    )

    assert chunks, "HybridChunker returned no chunks."

    # --------------------------------------------------------
    # 3. Basic validation
    # --------------------------------------------------------

    assert isinstance(chunks, list)

    for chunk in chunks:

        assert "chunk_index" in chunk
        assert "document_id" in chunk
        assert "file_name" in chunk
        assert "text" in chunk
        assert "metadata" in chunk

        assert chunk["text"].strip()

    # --------------------------------------------------------
    # 4. Display results
    # --------------------------------------------------------

    print(f"Total chunks: {len(chunks)}")

    print("\n" + "=" * 70)
    print("CHUNKS")
    print("=" * 70)

    for chunk in chunks:

        print(f"\nChunk Index : {chunk['chunk_index']}")
        print(f"File Name   : {chunk['file_name']}")

        print("-" * 70)
        print(chunk["text"])

        print("-" * 70)
        print("Metadata:")
        print(chunk["metadata"])

        print("=" * 70)

    print("\n✅ HYBRID CHUNKING TEST PASSED")


# ============================================================
# RUN TEST
# ============================================================

if __name__ == "__main__":
    test_hybrid_chunking()