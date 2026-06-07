from pathlib import Path

from security_utils import find_sensitive_markers, normalize_input_text, validate_public_sources
from ui_components import WELCOME_CAPTIONS, ensure_welcome_caption_file


def test_normalize_input_text_truncates_long_text():
    text = "A" * 9000
    cleaned = normalize_input_text(text, max_characters=100)
    assert len(cleaned) > 100
    assert "Text truncated" in cleaned


def test_find_sensitive_markers_flags_common_risks():
    markers = find_sensitive_markers("Example SSN 123-45-6789 and OPENAI_API_KEY should not be pasted.")
    assert "possible SSN" in markers
    assert "possible API key" in markers


def test_validate_public_sources_blocks_sensitive_text():
    sources = [
        {
            "label": "Source 1",
            "text": "This public alert includes something that should not be pasted: 123-45-6789.",
        }
    ]
    errors, warnings = validate_public_sources(sources)
    assert errors
    assert any("Source 1" in error for error in errors)


def test_validate_public_sources_requires_one_source():
    errors, warnings = validate_public_sources([])
    assert errors
    assert "Paste at least one" in errors[0]


def test_caption_file_is_valid_webvtt(tmp_path: Path):
    caption_path = tmp_path / "welcome_captions.vtt"
    ensure_welcome_caption_file(caption_path)
    content = caption_path.read_text(encoding="utf-8")
    assert content.startswith("WEBVTT")
    assert "TrendLens AI" in content
    assert "-->" in content


def test_embedded_caption_constant_is_valid_webvtt():
    assert WELCOME_CAPTIONS.startswith("WEBVTT")
    assert "information overload" in WELCOME_CAPTIONS
