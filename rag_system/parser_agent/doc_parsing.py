
import logging
from pathlib import Path

from docling.document_converter import DocumentConverter

logger = logging.getLogger(__name__)


def file_parsing(file_path: str):
    """
    Parse a PDF using Docling and return the DoclingDocument object.
    """

    if not file_path:
        raise ValueError("File path is required")

    if not Path(file_path).is_file():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    logger.info("Parsing document")

    converter = DocumentConverter()
    result = converter.convert(file_path)

    # Keep the DoclingDocument object for downstream chunking.
    parsed_file = result.document

    if parsed_file is None:
        raise ValueError("Docling failed to parse the document")

    # Validate extracted text without replacing the document object.
    extracted_text = parsed_file.export_to_markdown()

    if not extracted_text.strip():
        raise ValueError("No text could be extracted from the PDF")

    logger.info(
        "Document parsed successfully | characters=%d",
        len(extracted_text),
    )

    return parsed_file
