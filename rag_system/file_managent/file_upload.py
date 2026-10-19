import hashlib
import logging
from pathlib import Path

from File_manager_system.file_validation import (
    validate_extension,
    validate_file_size,
    validate_magic_bytes,
)

logger = logging.getLogger(__name__)


def generate_file_hash(uploaded_file: str) -> str:
    """Generate SHA-256 without loading the entire file into memory."""
    path = Path(uploaded_file)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {uploaded_file}")

    sha256 = hashlib.sha256()

    with path.open("rb") as file_handle:
        for chunk in iter(
            lambda: file_handle.read(1024 * 1024), b""
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


def file_checking(uploaded_file: str) -> dict:
    """Validate a single uploaded file and return its metadata."""
    filename = Path(uploaded_file).name

    try:
        validate_extension(uploaded_file)
        validate_file_size(uploaded_file)
        validate_magic_bytes(uploaded_file)

        file_hash = generate_file_hash(uploaded_file)

        validated_file = {
            "file_path": str(Path(uploaded_file)),
            "file_name": filename,
            "file_hash": file_hash,
        }

        logger.info(
            "File validation successful | file=%s | sha256=%s",
            filename,
            file_hash,
        )

        return validated_file

    except Exception:
        logger.exception(
            "File validation failed | file=%s",
            filename,
        )
        raise
    
