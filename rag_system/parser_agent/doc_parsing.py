import logging

from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
)

logger = logging.getLogger(__name__)


def create_converter() -> DocumentConverter:
    """Create a Docling converter with OCR enabled."""

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.generate_picture_images = True

    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options
            )
        }
    )


def file_parsing(document):
    """Parse a document and return Markdown content."""

    if document is None:
        raise ValueError("Document cannot be empty")

    logger.info("Parsing document")

    converter = create_converter()
    result = converter.convert(document)

    parsed_file = result.document

    if not parsed_file.strip():
        raise ValueError("No content extracted from document")

    logger.info("Document parsing completed")

    return parsed_file