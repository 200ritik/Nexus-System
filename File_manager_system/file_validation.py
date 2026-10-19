
from pathlib import Path
import logging

from configuration.config import (
    MAX_SIZE_MB,
    MAX_FILE,
    ALLOWED_EXTENSIONS,
    FILE_SIGNATURES,
)

logger = logging.getLogger(__name__)

# ============ max file allowed ==================
# ================================================
def max_file_allowed(uploaded_file: list[str]) -> list[str]:
    """Allow one file per request."""
    if not uploaded_file:
        raise ValueError("At least one file must be provided.")

    if len(uploaded_file) > MAX_FILE:
        raise ValueError(
            f"Maximum {MAX_FILE} file(s) are allowed per upload."
        )

    return uploaded_file


# =============== check file extension ===============
# ====================================================

def validate_extension(uploaded_file: str) -> bool:
    """Validate the file extension."""
    extension = Path(uploaded_file).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"File type '{extension}' is not allowed."
        )

    return True

# ============== validate the file size =====================
# ===========================================================

def validate_file_size(uploaded_file: str) -> bool:
    """Validate file existence and maximum size."""
    file_path = Path(uploaded_file)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"File not found: {uploaded_file}"
        )

    size_mb = file_path.stat().st_size / (1024 * 1024)

    if size_mb > MAX_SIZE_MB:
        raise ValueError(
            f"{file_path.name} is {size_mb:.2f} MB; "
            f"maximum allowed size is {MAX_SIZE_MB} MB."
        )

    return True

# ====================== Verify the content =======================
# =================================================================

def validate_magic_bytes(uploaded_file: str) -> bool:
    """Verify that file content matches its extension."""
    file_path = Path(uploaded_file)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"File not found: {uploaded_file}"
        )

    extension = file_path.suffix.lower()
    signatures = FILE_SIGNATURES.get(extension)

    if not signatures:
        raise ValueError(
            f"No magic-byte validation configured for {extension}"
        )

    bytes_to_read = max(
        len(signature) for signature in signatures
    )

    with file_path.open("rb") as file_handle:
        header = file_handle.read(bytes_to_read)

    if not any(
        header.startswith(signature)
        for signature in signatures
    ):
        raise ValueError(
            f"File content does not match extension {extension}."
        )

    return True
