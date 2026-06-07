"""UI helper components for TrendLens AI.

Adds a short welcome-video block with subtitles/captions.
The video autoplays muted because browsers commonly block autoplay with sound.
Users can turn sound on using the browser video controls.
"""

from pathlib import Path

ASSETS_DIR = Path("assets")
WELCOME_VIDEO_PATH = ASSETS_DIR / "welcome_video.mp4"
WELCOME_CAPTIONS_PATH = ASSETS_DIR / "welcome_captions.vtt"

WELCOME_SCRIPT = """Need to turn scattered public updates into a clear situation report fast?
Welcome to TrendLens AI, a public-source situational awareness assistant built to help users compare reports, identify key facts, highlight gaps, and generate structured intelligence-style summaries.
To use the site, start by choosing your audience and report purpose. Then paste up to three public sources, such as alerts, articles, reports, or updates. Select the sections you want, then generate your report.
TrendLens AI will organize the information into a clear BLUF, source comparison, confidence assessment, risks, follow-up questions, and a short brief.
Use only public or synthetic information. Do not enter classified, private, sensitive, or restricted data.
TrendLens AI helps you move from information overload to a focused, usable report."""

WELCOME_CAPTIONS = """WEBVTT

00:00:00.000 --> 00:00:04.500
Need to turn scattered public updates into a clear situation report fast?

00:00:04.500 --> 00:00:11.500
Welcome to TrendLens AI, a public-source situational awareness assistant built to compare reports, identify facts, highlight gaps, and generate intelligence-style summaries.

00:00:11.500 --> 00:00:20.500
Start by choosing your audience and report purpose. Then paste up to three public sources, such as alerts, articles, reports, or updates.

00:00:20.500 --> 00:00:29.500
Select the sections you want, then generate your report. TrendLens AI will organize the information into a BLUF, source comparison, confidence assessment, risks, RFIs, and a short brief.

00:00:29.500 --> 00:00:37.000
Use only public or synthetic information. Do not enter classified, private, sensitive, or restricted data.

00:00:37.000 --> 00:00:42.000
TrendLens AI helps you move from information overload to a focused, usable report.
"""


def ensure_welcome_caption_file(path: Path = WELCOME_CAPTIONS_PATH) -> Path:
    """Create the default WebVTT caption file if it does not exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(WELCOME_CAPTIONS, encoding="utf-8")
    return path


def render_welcome_video() -> None:
    """Render the welcome video if present; otherwise render a helpful placeholder.

    Keep the Streamlit import inside this function so tests can import this module
    without needing a running Streamlit context.
    """
    import streamlit as st

    ASSETS_DIR.mkdir(exist_ok=True)
    caption_path = ensure_welcome_caption_file()

    with st.expander("Welcome video and quick start", expanded=True):
        st.markdown(
            """
            **TrendLens AI** turns public or synthetic source text into a structured
            situational awareness report. The intro video autoplays muted, and users
            can turn sound on with the video controls.
            """
        )

        if WELCOME_VIDEO_PATH.exists() and WELCOME_VIDEO_PATH.stat().st_size > 0:
            st.video(
                data=str(WELCOME_VIDEO_PATH),
                format="video/mp4",
                subtitles=str(caption_path),
                autoplay=True,
                muted=True,
                loop=False,
                width="stretch",
            )
            st.caption(
                "Subtitles are enabled by default. The video starts muted because most browsers block autoplay with sound."
            )
        else:
            st.info(
                "Welcome video placeholder: add assets/welcome_video.mp4 to enable the intro video. "
                "The subtitle file assets/welcome_captions.vtt is already prepared."
            )
            with st.expander("Voiceover script"):
                st.write(WELCOME_SCRIPT)
