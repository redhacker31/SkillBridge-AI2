"""
SkillBridge AI — Resume Parser (Module 1)

Extracts readable text from uploaded PDF resumes.
Primary: PyMuPDF (fitz) — fast, reliable.
Fallback: pdfplumber — handles complex layouts.

This module is independent of FastAPI.
"""

import logging
from pathlib import Path

logger = logging.getLogger("skillbridge.ai.parser")


def extract_text_pymupdf(pdf_path: str) -> str:
    """Extract text from a PDF using PyMuPDF (fitz)."""
    import fitz  # PyMuPDF

    text_parts: list[str] = []
    doc = fitz.open(pdf_path)
    try:
        for page_num in range(len(doc)):
            page = doc[page_num]
            # 'blocks' preserves paragraph structure better than raw 'text'
            blocks = page.get_text("blocks", sort=True)
            for b in blocks:
                # b[4] is the text of the block
                if isinstance(b[4], str) and b[4].strip():
                    # Clean up the text block: replace multiple spaces with single, 
                    # but preserve intentional newlines within the block if any, or just strip it
                    clean_block = " ".join(b[4].split())
                    text_parts.append(clean_block)
    finally:
        doc.close()

    return "\n".join(text_parts)


def extract_text_pdfplumber(pdf_path: str) -> str:
    """Fallback: extract text from a PDF using pdfplumber."""
    import pdfplumber

    text_parts: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts)


def extract_text(pdf_path: str) -> str:
    """
    Extract text from a PDF file.

    Tries PyMuPDF first. Falls back to pdfplumber if PyMuPDF fails
    or returns empty text.

    Args:
        pdf_path: Absolute or relative path to the PDF file.

    Returns:
        Extracted plain text from the PDF.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ValueError: If no text could be extracted from the PDF.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Try PyMuPDF first
    text = ""
    try:
        text = extract_text_pymupdf(pdf_path)
        logger.info("Text extracted successfully using PyMuPDF (%d chars)", len(text))
    except Exception as e:
        logger.warning("PyMuPDF extraction failed: %s. Trying pdfplumber...", e)

    # Fallback to pdfplumber if PyMuPDF produced no text
    if not text.strip():
        try:
            text = extract_text_pdfplumber(pdf_path)
            logger.info("Text extracted using pdfplumber fallback (%d chars)", len(text))
        except Exception as e:
            logger.error("pdfplumber extraction also failed: %s", e)
            raise ValueError(f"Could not extract text from PDF: {pdf_path}") from e

    if not text.strip():
        raise ValueError(f"PDF appears to contain no extractable text: {pdf_path}")

    return text.strip()
