
import logging
import re
from urllib.parse import urlparse

import requests
import trafilatura
from bs4 import BeautifulSoup
from langchain.tools import tool
from readability import Document

logger = logging.getLogger(__name__)

MAX_TEXT_LENGTH = 10000
MIN_TEXT_LENGTH = 200
REQUEST_TIMEOUT = 15

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MedicalResearchBot/1.0)",
    "Accept-Language": "en-US,en;q=0.9",
}

UNWANTED_TAGS = [
    "script",
    "style",
    "nav",
    "footer",
    "header",
    "aside",
    "form",
    "noscript",
]


def clean_text(text: str) -> str:
    """Normalize whitespace in extracted text."""
    return re.sub(r"\s+", " ", text).strip()


def remove_unwanted_tags(soup: BeautifulSoup) -> None:
    """Remove elements that rarely contain article content."""
    for tag in soup(UNWANTED_TAGS):
        tag.decompose()


def validate_url(url: str) -> bool:
    """Allow only public HTTP/HTTPS URLs."""
    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return False

        if not parsed.hostname or parsed.username or parsed.password:
            return False

        hostname = parsed.hostname.lower()

        if hostname == "localhost" or hostname.endswith(".localhost"):
            return False

        if hostname.endswith(".local"):
            return False

        # Reject literal private, loopback, and reserved IP addresses.
        import ipaddress

        try:
            address = ipaddress.ip_address(hostname)
            if not address.is_global:
                return False
        except ValueError:
            pass

        return True

    except (ValueError, TypeError):
        return False


def extract_with_trafilatura(html: str) -> str:
    text = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=True,
    )
    return clean_text(text) if text else ""


def extract_with_readability(html: str) -> str:
    document = Document(html)
    soup = BeautifulSoup(document.summary(), "html.parser")
    remove_unwanted_tags(soup)

    return clean_text(
        soup.get_text(separator=" ", strip=True)
    )


def extract_with_beautifulsoup(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    remove_unwanted_tags(soup)

    return clean_text(
        soup.get_text(separator=" ", strip=True)
    )


@tool
def scrape_url(url: str) -> str:
    """
    Extract readable text from one medical or health webpage.
    Use a URL discovered by the research search tool.
    Returns extracted text and the source URL.
    """

    if not validate_url(url):
        return "Error: Invalid or unsupported URL."

    try:
        with requests.Session() as session:
            response = session.get(
                url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=True,
            )
            response.raise_for_status()

            # Validate the final destination after redirects.
            if not validate_url(response.url):
                return "Error: Redirected to an unsupported URL."

            content_type = response.headers.get(
                "Content-Type", ""
            ).lower()

            if "text/html" not in content_type:
                return (
                    "Unsupported content type. "
                    "Expected an HTML webpage."
                )

            html = response.text

        # Strategy 1: Trafilatura
        extracted_text = extract_with_trafilatura(html)

        # Strategy 2: Readability
        if len(extracted_text) < MIN_TEXT_LENGTH:
            extracted_text = extract_with_readability(html)

        # Strategy 3: BeautifulSoup fallback
        if len(extracted_text) < MIN_TEXT_LENGTH:
            extracted_text = extract_with_beautifulsoup(html)

        if not extracted_text:
            return (
                f"No meaningful content could be extracted. "
                f"Source: {response.url}"
            )

        if len(extracted_text) > MAX_TEXT_LENGTH:
            extracted_text = extracted_text[:MAX_TEXT_LENGTH]

        return (
            f"Source URL: {response.url}\n"
            f"Extracted content:\n{extracted_text}"
        )

    except requests.exceptions.Timeout:
        logger.warning("Page extraction timed out: %s", url)
        return "Error: The webpage request timed out."

    except requests.exceptions.HTTPError as exc:
        logger.warning("HTTP error extracting %s: %s", url, exc)
        return "Error: The webpage returned an HTTP error."

    except requests.exceptions.RequestException:
        logger.exception("Request failed for URL: %s", url)
        return "Error: Unable to fetch the webpage."

    except Exception:
        logger.exception("Content extraction failed for URL: %s", url)
        return "Error: Unable to extract webpage content."
