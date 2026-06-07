"""Input safety and validation helpers for TrendLens AI."""

import re
from typing import Iterable

MAX_SOURCE_CHARACTERS = 8000
MIN_SOURCE_CHARACTERS = 40

PUBLIC_ONLY_WARNING = (
    "Use only public or synthetic information. Do not paste classified, private, "
    "sensitive, restricted, protected, or personal information."
)

SENSITIVE_PATTERNS = [
    ("possible SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("possible credit card number", re.compile(r"\b(?:\d[ -]*?){13,16}\b")),
    ("possible classified marking", re.compile(r"\b(TOP SECRET|SECRET|CONFIDENTIAL|NOFORN|CUI|FOUO)\b", re.I)),
    ("possible private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", re.I)),
    ("possible API key", re.compile(r"\b(?:sk-|OPENAI_API_KEY|api[_-]?key|client[_-]?secret)\b", re.I)),
]


def normalize_input_text(text: str, max_characters: int = MAX_SOURCE_CHARACTERS) -> str:
    """Normalize user text and limit excessive input size."""
    cleaned = str(text or "").replace("\r\n", "\n").replace("\r", "\n")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    if len(cleaned) > max_characters:
        cleaned = cleaned[:max_characters] + "\n\n[Text truncated at project input size limit.]"
    return cleaned


def find_sensitive_markers(text: str) -> list[str]:
    """Return labels for high-risk content patterns detected in text."""
    markers = []
    for label, pattern in SENSITIVE_PATTERNS:
        if pattern.search(text or ""):
            markers.append(label)
    return markers


def validate_public_sources(sources: Iterable[dict]) -> tuple[list[str], list[str]]:
    """Validate source inputs before sending to the model.

    Returns:
        errors: blocks report generation.
        warnings: allows report generation but should be shown to the user.
    """
    errors: list[str] = []
    warnings: list[str] = []
    usable_count = 0

    for index, source in enumerate(sources or [], start=1):
        text = normalize_input_text(source.get("text", ""))
        label = source.get("label", f"Source {index}")

        if text:
            usable_count += 1

        if text and len(text) < MIN_SOURCE_CHARACTERS:
            warnings.append(f"{label}: source text is very short, so confidence may be limited.")

        markers = find_sensitive_markers(text)
        if markers:
            errors.append(
                f"{label}: remove high-risk content before generating the report. Detected: {', '.join(markers)}."
            )

    if usable_count == 0:
        errors.append("Paste at least one public or synthetic source before generating a report.")

    return errors, warnings
