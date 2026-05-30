import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

PROJECT_ROOT = Path(__file__).parent
PROMPTS_DIR = PROJECT_ROOT / "Prompts"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

OUTPUTS_DIR.mkdir(exist_ok=True)


def load_prompt(prompt_name: str) -> str:
    """
    Loads a prompt file from the Prompts folder.
    """
    prompt_path = PROMPTS_DIR / prompt_name

    if not prompt_path.exists():
        return ""

    return prompt_path.read_text(encoding="utf-8")


def clean_source_text(text: str) -> str:
    """
    Cleans pasted source text so the model receives a clearer input.
    This function acts as the source cleaning tool.
    """
    if not text:
        return ""

    cleaned = text.strip()
    cleaned = "\n".join(line.strip() for line in cleaned.splitlines() if line.strip())

    return cleaned


def build_source_block(source_label: str, source_url: str, source_text: str) -> str:
    """
    Creates one structured source block for the model.
    This function acts as the source intake formatting tool.
    """
    cleaned_text = clean_source_text(source_text)

    return f"""
SOURCE LABEL:
{source_label if source_label else "Not provided"}

SOURCE URL:
{source_url if source_url else "Not provided"}

SOURCE TEXT:
{cleaned_text if cleaned_text else "No source text provided"}
"""


def build_combined_sources(sources: list[dict]) -> str:
    """
    Combines all user submitted sources into one structured input.
    This function acts as the source consolidation tool.
    """
    source_blocks = []

    for index, source in enumerate(sources, start=1):
        source_blocks.append(
            f"""
==============================
SOURCE {index}
==============================
{build_source_block(
    source_label=source.get("label", ""),
    source_url=source.get("url", ""),
    source_text=source.get("text", "")
)}
"""
        )

    return "\n".join(source_blocks)


def build_report_prompt(sources: list[dict]) -> str:
    """
    Builds the full user prompt for the TrendLens report.
    This function acts as the prompt routing tool.
    """
    combined_sources = build_combined_sources(sources)
    report_template = load_prompt("report_prompt.md")

    if not report_template:
        report_template = """
Create a structured TrendLens AI Report with source overview, Bottom Line Up Front, executive summary, so what, key trends, risks or concerns, confidence level, follow up questions, and a 45 second brief.
"""

    return f"""
Analyze the public information sources below and create one unified TrendLens AI situational awareness report.

Use the report format and rules below.

REPORT FORMAT AND RULES:
{report_template}

Important:
Only use information from the provided sources.
Do not invent facts.
If dates, locations, actors, or outcomes are missing, say not provided.
Do not force unrelated events into one false narrative.
Focus on significance, patterns, uncertainty, and follow up questions.

SOURCES:
{combined_sources}
"""


def generate_trendlens_report(sources: list[dict]) -> str:
    """
    Sends the structured source information to OpenAI and returns the report.
    This function acts as the report generation tool.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "Error: OPENAI_API_KEY was not found. Check the .env file."

    client = OpenAI(api_key=api_key)

    system_prompt = load_prompt("system_prompt.md")

    if not system_prompt:
        system_prompt = """
You are TrendLens AI, an agentic situational awareness assistant.
Your role is to transform public information into structured analyst style reporting products.
You prioritize clarity, uncertainty, pattern recognition, and practical briefing value.
You do not invent facts.
"""

    user_prompt = build_report_prompt(sources)

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.3,
        )

        return response.output_text

    except Exception as error:
        return f"Error generating report: {error}"


def get_agent_workflow_summary(sources: list[dict]) -> str:
    """
    Explains the lightweight agent workflow used by TrendLens AI.
    This makes the agentic design visible in the app.
    """
    source_count = len(sources)

    return f"""
TrendLens AI used a lightweight agentic workflow for this analysis.

1. Source intake tool: collected {source_count} submitted public information source(s).

2. Source cleaning tool: removed extra spacing and prepared the text for analysis.

3. Source consolidation tool: combined the submitted sources into one structured source block.

4. Prompt routing tool: combined the source material with the system prompt and report prompt.

5. Reasoning tool: directed the model to identify significance, patterns, risks, confidence, and follow up questions.

6. Report generation tool: created one structured situational awareness report.

7. Memory tool: stored the latest report in the current Streamlit session.

8. Feedback tool: allows the user to save feedback for evaluation and later improvement.
"""


def save_report(report_text: str) -> str:
    """
    Saves the latest report as a markdown file in the outputs folder.
    This function acts as the report saving tool.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = OUTPUTS_DIR / f"trendlens_report_{timestamp}.md"

    file_path.write_text(report_text, encoding="utf-8")

    return str(file_path)


def save_feedback(feedback: str, notes: str = "") -> str:
    """
    Saves basic user feedback for evaluation and future improvement.
    This function acts as the feedback logging tool.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_path = OUTPUTS_DIR / "feedback_log.csv"

    new_file = not feedback_path.exists()

    with feedback_path.open("a", encoding="utf-8") as file:
        if new_file:
            file.write("timestamp,feedback,notes\n")

        safe_feedback = feedback.replace(",", " ")
        safe_notes = notes.replace(",", " ").replace("\n", " ")

        file.write(f"{timestamp},{safe_feedback},{safe_notes}\n")

    return str(feedback_path)