import csv
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI


try:
    import requests
except ImportError:
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


load_dotenv()

PROJECT_ROOT = Path(__file__).parent
PROMPTS_DIR = PROJECT_ROOT / "Prompts"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

OUTPUTS_DIR.mkdir(exist_ok=True)

MAX_SOURCE_CHARACTERS = 8000


def load_prompt(prompt_name: str) -> str:
    """
    Loads a prompt file from the Prompts folder.
    """
    prompt_path = PROMPTS_DIR / prompt_name

    if not prompt_path.exists():
        return ""

    return prompt_path.read_text(encoding="utf-8")


def clean_source_text(text: str, max_characters: int = MAX_SOURCE_CHARACTERS) -> str:
    """
    Cleans pasted or extracted source text so the model receives a clearer input.
    This function acts as the source cleaning tool.
    """
    if not text:
        return ""

    cleaned = text.strip()
    cleaned = re.sub(r"\r\n", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = "\n".join(line.strip() for line in cleaned.splitlines() if line.strip())

    if len(cleaned) > max_characters:
        cleaned = (
            cleaned[:max_characters]
            + "\n\n[Source text truncated because it exceeded the project input size limit.]"
        )

    return cleaned


def extract_text_from_url(url: str) -> tuple[str, str]:
    """
    Attempts to extract readable article text from a public URL.

    This is intentionally lightweight for the class project.
    If extraction fails, the app still works with pasted text.
    """
    if not url:
        return "", "No URL provided."

    if not url.startswith(("http://", "https://")):
        return "", "URL was not fetched because it does not start with http:// or https://."

    if requests is None or BeautifulSoup is None:
        return (
            "",
            "URL text extraction was skipped because requests or BeautifulSoup is not installed.",
        )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 TrendLensAI/1.0 "
            "(student research project; public source summarization)"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        paragraphs = [
            paragraph.get_text(" ", strip=True)
            for paragraph in soup.find_all("p")
            if paragraph.get_text(" ", strip=True)
        ]

        if paragraphs:
            extracted_text = "\n".join(paragraphs)
        else:
            extracted_text = soup.get_text("\n", strip=True)

        cleaned_text = clean_source_text(extracted_text)

        if not cleaned_text:
            return "", "URL was reached, but no readable text was extracted."

        return cleaned_text, "URL text extracted successfully."

    except Exception as error:
        return "", f"URL text extraction failed: {error}"


def build_source_block(source_number: int, source: dict) -> str:
    """
    Creates one structured source block for the model.
    This function acts as the source intake formatting tool.
    """
    source_type = source.get("type", "Other public source")
    source_label = source.get("label", "")
    source_url = source.get("url", "")
    source_text = source.get("text", "")

    cleaned_text = clean_source_text(source_text)
    extraction_status = "Pasted source text used."

    if not cleaned_text and source_url:
        cleaned_text, extraction_status = extract_text_from_url(source_url)

    if not cleaned_text:
        cleaned_text = (
            "No source text was provided or extracted. Use only the available label, "
            "source type, and URL metadata. Do not infer article details from the URL alone."
        )

    return f"""
SOURCE {source_number} TYPE:
{source_type if source_type else "Not provided"}

SOURCE {source_number} LABEL:
{source_label if source_label else "Not provided"}

SOURCE {source_number} URL:
{source_url if source_url else "Not provided"}

SOURCE {source_number} EXTRACTION STATUS:
{extraction_status}

SOURCE {source_number} TEXT:
{cleaned_text}
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
{build_source_block(index, source)}
"""
        )

    return "\n".join(source_blocks)


def format_selected_outputs(selected_outputs: Optional[dict]) -> str:
    """
    Converts selected report sections into clean text for the prompt.
    """
    default_sections = [
        "BLUF",
        "Executive Summary",
        "5 Ws",
        "Key Judgments",
        "Key Trends",
        "Source Comparison and Reliability Notes",
        "Risks and Concerns",
        "Second Order Effects",
        "Third Order Effects",
        "Indicators",
        "Assessment",
        "Collection Gaps",
        "Confidence Assessment",
        "Recommended Follow Up Questions",
    ]

    if not selected_outputs:
        selected_sections = default_sections
    else:
        selected_sections = [
            section for section, enabled in selected_outputs.items() if enabled
        ]

        if not selected_sections:
            selected_sections = default_sections

    return "\n".join(f"{index}. {section}" for index, section in enumerate(selected_sections, start=1))


def build_report_prompt(
    sources: list[dict],
    user_role: str = "Intelligence Analyst",
    report_purpose: str = "",
    selected_outputs: Optional[dict] = None,
    custom_output_request: str = "",
) -> str:
    """
    Builds the full user prompt for the TrendLens report.
    This function acts as the prompt routing tool.
    """
    combined_sources = build_combined_sources(sources)
    selected_sections_text = format_selected_outputs(selected_outputs)
    report_template = load_prompt("report_prompt.md")

    if not report_template:
        report_template = """
Create a structured TrendLens AI situational awareness report. Use the selected report sections requested by the user. Include source comparison, analytical significance, uncertainty, confidence level, and recommended follow up questions when those sections are selected.
"""

    return f"""
Analyze the public information sources below and create one unified TrendLens AI situational awareness report.

USER ROLE:
{user_role if user_role else "Not provided"}

REPORT PURPOSE:
{report_purpose if report_purpose else "Not provided"}

REQUESTED OUTPUT SECTIONS:
{selected_sections_text}

ADDITIONAL USER REQUEST:
{custom_output_request if custom_output_request else "None provided"}

REPORT FORMAT GUIDANCE:
{report_template}

CORE ANALYTIC REQUIREMENTS:
1. Only use information from the provided sources.
2. Do not invent facts, dates, locations, actors, motives, outcomes, or source claims.
3. If important information is missing, state that it is not provided.
4. Do not force unrelated sources into one false narrative.
5. Compare the sources directly.
6. Identify where sources agree.
7. Identify where sources conflict.
8. Identify what information still needs confirmation.
9. Identify the significance of the event or topic based on the selected user role.
10. Tailor wording to the selected user role and report purpose.
11. Use clear intelligence style writing.
12. Avoid exaggerated language.
13. Use plain language that a non specialist could still understand.
14. Do not include classified methods, classified assumptions, or restricted information.

SOURCE COMPARISON REQUIREMENTS:
Include direct comparison across sources when possible. Explain what is consistent, what is uncertain, what appears incomplete, and whether the reporting suggests a developing event.

CONFIDENCE ASSESSMENT RULES:
Use these confidence bands if the confidence assessment section is selected.

High confidence means 80 to 100 percent. Multiple reliable sources agree, major facts are consistent, and the available information supports the assessment.

Moderate confidence means 50 to 79 percent. Some source agreement exists, but gaps, early reporting, unclear details, or limited corroboration remain.

Low confidence means 0 to 49 percent. Reporting is limited, conflicting, early, difficult to verify, or based on incomplete source material.

When assigning confidence, explain why that confidence level was selected. Do not give a percentage without explaining the reason.

GRAPHICAL SUMMARY TABLE RULE:
If the user selected Graphical Summary Table, create a markdown table. Do not claim to generate actual images, maps, or charts unless the application has created them.

SOURCES:
{combined_sources}
"""


def generate_trendlens_report(
    sources: list[dict],
    user_role: str = "Intelligence Analyst",
    report_purpose: str = "",
    selected_outputs: Optional[dict] = None,
    custom_output_request: str = "",
) -> str:
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
You are TrendLens AI, a structured public information analysis agent.

Your role is to transform public information sources into customized situational awareness products. You support multi source intake, source normalization, source comparison, trend extraction, risk assessment, confidence assessment, and report generation.

You prioritize accuracy, clarity, uncertainty management, source comparison, and practical briefing value.

You do not invent facts. You do not treat unverified information as confirmed. You do not use classified, private, sensitive, or restricted information.
"""

    user_prompt = build_report_prompt(
        sources=sources,
        user_role=user_role,
        report_purpose=report_purpose,
        selected_outputs=selected_outputs,
        custom_output_request=custom_output_request,
    )

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
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

    source_type_lines = []
    for index, source in enumerate(sources, start=1):
        source_type = source.get("type", "Other public source")
        source_label = source.get("label", "No label provided")
        source_type_lines.append(f"{index}. {source_type}: {source_label}")

    source_type_summary = "\n".join(source_type_lines) if source_type_lines else "No sources submitted."

    return f"""
TrendLens AI used one main TrendLens Analysis Agent for this report.

Submitted source count:
{source_count}

Submitted source types:
{source_type_summary}

Workflow used:

1. Source Intake
Collected the submitted public information sources, source labels, source types, URLs, and pasted text.

2. Source Normalization
Cleaned the source text and prepared the material for analysis.

3. Source Enrichment
Attempted lightweight URL text extraction when a URL was provided without pasted text.

4. Source Consolidation
Combined all submitted sources into one structured source block.

5. Source Comparison
Directed the model to compare where sources agree, disagree, or leave information gaps.

6. Trend Extraction
Directed the model to identify key trends, indicators, patterns, and significant changes.

7. Risk and Impact Assessment
Directed the model to assess risks, concerns, safety considerations, and possible second and third order effects when requested.

8. Confidence Assessment
Directed the model to assign high, moderate, or low confidence using explicit percentage bands and reasoning.

9. Report Generation
Generated one customized situational awareness report based on the selected role, report purpose, and requested output sections.

10. Session Memory
Stored the latest report and workflow summary in the current Streamlit session.

11. Feedback Logging
Allows the user to save feedback for later evaluation and improvement.
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

    with feedback_path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        if new_file:
            writer.writerow(["timestamp", "feedback", "notes"])

        writer.writerow([timestamp, feedback, notes])

    return str(feedback_path)