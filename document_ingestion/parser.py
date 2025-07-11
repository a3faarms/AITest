"""Utilities for extracting text from PDF and Word documents."""

from pathlib import Path
from typing import Optional


class DocumentParser:
    """Parse documents and return extracted text."""

    def __init__(self) -> None:
        pass

    def parse(self, path: Path) -> Optional[str]:
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return self._parse_pdf(path)
        if suffix in {".docx", ".doc"}:
            return self._parse_docx(path)
        raise ValueError(f"Unsupported file type: {suffix}")

    def _parse_pdf(self, path: Path) -> str:
        try:
            from pdfminer.high_level import extract_text
        except ImportError as exc:
            raise ImportError("pdfminer.six is required: pip install pdfminer.six") from exc
        return extract_text(str(path))

    def _parse_docx(self, path: Path) -> str:
        try:
            import docx
        except ImportError as exc:
            raise ImportError("python-docx is required: pip install python-docx") from exc
        document = docx.Document(str(path))
        lines = [para.text for para in document.paragraphs]
        return "\n".join(lines)
