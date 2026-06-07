"""Generate the TrendLens AI welcome voiceover.

Run from the project root after setting OPENAI_API_KEY:
    python scripts/generate_welcome_voice.py

Output:
    assets/welcome_voice.mp3

Then combine the MP3 with visuals in Canva, Clipchamp, CapCut, or another editor
and export the finished file as:
    assets/welcome_video.mp4
"""

from pathlib import Path
from openai import OpenAI

VOICEOVER = """Need to turn scattered public updates into a clear situation report fast?

Welcome to TrendLens AI, a public-source situational awareness assistant built to help users compare reports, identify key facts, highlight gaps, and generate structured intelligence-style summaries.

To use the site, start by choosing your audience and report purpose. Then paste up to three public sources, such as alerts, articles, reports, or updates. Select the sections you want, then generate your report.

TrendLens AI will organize the information into a clear BLUF, source comparison, confidence assessment, risks, follow-up questions, and a short brief.

Use only public or synthetic information. Do not enter classified, private, sensitive, or restricted data.

TrendLens AI helps you move from information overload to a focused, usable report."""


def main() -> None:
    output_dir = Path("assets")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "welcome_voice.mp3"

    client = OpenAI()

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=VOICEOVER,
        instructions=(
            "Speak in a professional, calm, confident briefing style. "
            "Start with an attention-grabbing tone, then become clear and instructional. "
            "Use a smooth, polished ending."
        ),
    ) as response:
        response.stream_to_file(output_path)

    print(f"Saved voiceover to {output_path}")


if __name__ == "__main__":
    main()
