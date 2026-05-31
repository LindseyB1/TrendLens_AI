import csv
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

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
OUTPUTS_DIR = PROJECT_ROOT / "Outputs"
DATA_DIR = PROJECT_ROOT / "Data"
TESTS_DIR = PROJECT_ROOT / "Tests"

PROMPTS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
TESTS_DIR.mkdir(exist_ok=True)

MAX_SOURCE_CHARACTERS = 8000
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def ensure_project_folders():
    PROMPTS_DIR.mkdir(exist_ok=True)
    OUTPUTS_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)
    TESTS_DIR.mkdir(exist_ok=True)


def load_prompt(prompt_name: str) -> str:
    prompt_path = PROMPTS_DIR / prompt_name

    if not prompt_path.exists():
        return ""

    try:
        return prompt_path.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def safe_filename(text: str, default_name: str = "trendlens_report") -> str:
    if not text:
        return default_name

    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", str(text).lower()).strip("_")

    if not cleaned:
        return default_name

    return cleaned[:80]


def clean_source_text(text: str, max_characters: int = MAX_SOURCE_CHARACTERS) -> str:
    if not text:
        return ""

    cleaned = str(text).strip()
    cleaned = re.sub(r"\r\n", "\n", cleaned)
    cleaned = re.sub(r"\r", "\n", cleaned)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = "\n".join(line.strip() for line in cleaned.splitlines() if line.strip())

    if len(cleaned) > max_characters:
        cleaned = (
            cleaned[:max_characters]
            + "\n\n[Source text truncated because it exceeded the project input size limit.]"
        )

    return cleaned


def normalize_text(text: str) -> str:
    return clean_source_text(text, max_characters=MAX_SOURCE_CHARACTERS)


def extract_text_from_url(url: str) -> tuple[str, str]:
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


def clean_sources(sources: Union[list[dict], str, None]) -> list[dict]:
    if sources is None:
        return []

    if isinstance(sources, str):
        cleaned_text = clean_source_text(sources)

        if not cleaned_text:
            return []

        return [
            {
                "source_number": 1,
                "type": "Public source text",
                "label": "Source 1",
                "url": "",
                "text": cleaned_text,
            }
        ]

    cleaned_sources = []

    if isinstance(sources, list):
        for index, source in enumerate(sources, start=1):
            if isinstance(source, dict):
                source_text = clean_source_text(source.get("text", ""))
                source_url = source.get("url", "").strip()
                source_label = source.get("label", f"Source {index}")
                source_type = source.get("type", "Other public source")

                if not source_text and not source_url and not source_label:
                    continue

                cleaned_sources.append(
                    {
                        "source_number": source.get("source_number", index),
                        "type": source_type,
                        "label": source_label,
                        "url": source_url,
                        "text": source_text,
                    }
                )

            elif isinstance(source, str):
                source_text = clean_source_text(source)

                if source_text:
                    cleaned_sources.append(
                        {
                            "source_number": index,
                            "type": "Public source text",
                            "label": f"Source {index}",
                            "url": "",
                            "text": source_text,
                        }
                    )

    return cleaned_sources


def build_source_block(source_number: int, source: dict) -> str:
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
    cleaned_sources = clean_sources(sources)
    source_blocks = []

    for index, source in enumerate(cleaned_sources, start=1):
        source_blocks.append(
            f"""
==============================
SOURCE {index}
==============================
{build_source_block(index, source)}
"""
        )

    if not source_blocks:
        return "No valid public source text was provided."

    return "\n".join(source_blocks)


def format_selected_outputs(
    selected_outputs: Optional[Union[dict, list[str]]]
) -> str:
    default_sections = [
        "Source Overview",
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

    elif isinstance(selected_outputs, dict):
        selected_sections = [
            section for section, enabled in selected_outputs.items() if enabled
        ]

        if not selected_sections:
            selected_sections = default_sections

    elif isinstance(selected_outputs, list):
        selected_sections = selected_outputs if selected_outputs else default_sections

    else:
        selected_sections = default_sections

    return "\n".join(
        f"{index}. {section}"
        for index, section in enumerate(selected_sections, start=1)
    )


def route_task(target_audience: str = "", task_type: str = "") -> str:
    audience = (target_audience or "").lower()
    task = (task_type or "").lower()

    if "monitor" in task or "update" in task:
        return "Monitoring Update Route"

    if "intelligence" in audience or "analyst" in audience:
        return "Intelligence Analyst Route"

    if "emergency" in audience:
        return "Emergency Responder Route"

    if "public" in audience:
        return "Public Audience Route"

    if "journalist" in audience:
        return "Journalist Route"

    if "research" in audience or "student" in audience:
        return "Research / Student Route"

    if "security" in audience:
        return "Security Professional Route"

    return "General Situational Awareness Route"


def get_route_instruction(model_route: str, target_audience: str, task_type: str) -> str:
    route = (model_route or "").lower()
    audience = (target_audience or "").lower()
    task = (task_type or "").lower()

    if "monitor" in route or "monitor" in task or "update" in task:
        return (
            "Use the monitoring update route. Focus on what changed, what stayed the same, "
            "why the change matters, and what should be reviewed by a human user."
        )

    if "intelligence" in route or "intelligence" in audience or "analyst" in audience:
        return (
            "Use the intelligence analyst route. Use structured intelligence style writing, "
            "include source comparison, confidence, gaps, second and third order effects, "
            "and clear Requests for Information."
        )

    if "emergency" in route or "emergency" in audience:
        return (
            "Use the emergency responder route. Focus on public safety impact, operational "
            "concerns, response considerations, infrastructure effects, and community risk."
        )

    if "public" in route or "public" in audience:
        return (
            "Use the public audience route. Use plain language, avoid jargon, explain why "
            "the event matters, and clearly separate confirmed details from unknowns."
        )

    if "journalist" in route or "research" in audience:
        return (
            "Use the research and journalism route. Focus on source comparison, missing facts, "
            "timeline clarity, attribution, and questions that require verification."
        )

    if "security" in route or "security" in audience:
        return (
            "Use the security professional route. Focus on risk, threat indicators, business "
            "impact, public safety implications, and follow up information needs."
        )

    return (
        "Use the general situational awareness route. Focus on clarity, source grounded "
        "analysis, confidence, and useful next questions."
    )


def build_report_prompt(
    sources: list[dict],
    user_role: str = "Intelligence Analyst",
    report_purpose: str = "",
    selected_outputs: Optional[Union[dict, list[str]]] = None,
    custom_output_request: str = "",
    task_type: str = "Generate situational awareness report",
    output_depth: str = "Standard",
    model_route: str = "",
) -> str:
    combined_sources = build_combined_sources(sources)
    selected_sections_text = format_selected_outputs(selected_outputs)
    report_template = load_prompt("report_prompt.md")

    if not model_route:
        model_route = route_task(user_role, task_type)

    route_instruction = get_route_instruction(model_route, user_role, task_type)

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

TASK TYPE:
{task_type if task_type else "Not provided"}

OUTPUT DEPTH:
{output_depth if output_depth else "Standard"}

MODEL ROUTE:
{model_route}

ROUTING INSTRUCTION:
{route_instruction}

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


def build_system_prompt(
    user_role: str = "Intelligence Analyst",
    task_type: str = "Generate situational awareness report",
    model_route: str = "",
) -> str:
    system_prompt = load_prompt("system_prompt.md")

    if not model_route:
        model_route = route_task(user_role, task_type)

    route_instruction = get_route_instruction(model_route, user_role, task_type)

    if not system_prompt:
        system_prompt = """
You are TrendLens AI, a structured public information analysis agent.

Your role is to transform public information sources into customized situational awareness products. You support multi source intake, source normalization, source comparison, trend extraction, risk assessment, confidence assessment, and report generation.

You prioritize accuracy, clarity, uncertainty management, source comparison, and practical briefing value.

You do not invent facts. You do not treat unverified information as confirmed. You do not use classified, private, sensitive, or restricted information.
"""

    return f"""
{system_prompt}

ROUTING INSTRUCTION:
{route_instruction}
""".strip()


def call_openai_model(system_prompt: str, user_prompt: str, model_name: str = "") -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY was not found. Check the .env file.")

    client = OpenAI(api_key=api_key)
    selected_model = model_name or DEFAULT_MODEL

    try:
        response = client.responses.create(
            model=selected_model,
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

        if hasattr(response, "output_text") and response.output_text:
            return response.output_text.strip()

    except Exception:
        pass

    response = client.chat.completions.create(
        model=selected_model,
        messages=[
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

    return response.choices[0].message.content.strip()


def get_first_sentences(text: str, limit: int = 3) -> list[str]:
    cleaned = clean_source_text(text)

    if not cleaned:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    return sentences[:limit]


def build_source_overview(sources: list[dict]) -> str:
    cleaned_sources = clean_sources(sources)

    if not cleaned_sources:
        return "No valid public source text was provided."

    lines = []

    for source in cleaned_sources:
        source_number = source.get("source_number", "")
        source_type = source.get("type", "Not specified")
        source_label = source.get("label", f"Source {source_number}")
        source_url = source.get("url", "")

        url_text = f" URL: {source_url}" if source_url else ""

        lines.append(
            f"Source {source_number}: {source_label}. Type: {source_type}.{url_text}"
        )

    return "\n".join(lines)


def build_fallback_report(
    sources: list[dict],
    user_role: str,
    report_purpose: str,
    selected_outputs: Optional[Union[dict, list[str]]],
    custom_output_request: str,
    task_type: str,
    output_depth: str,
    model_route: str,
    fallback_reason: str,
) -> str:
    cleaned_sources = clean_sources(sources)
    source_count = len(cleaned_sources)
    source_overview = build_source_overview(cleaned_sources)

    extracted_sentences = []

    for source in cleaned_sources:
        first_sentences = get_first_sentences(source.get("text", ""), limit=3)

        for sentence in first_sentences:
            extracted_sentences.append(
                f"Source {source.get('source_number')}: {sentence}"
            )

    if not extracted_sentences:
        extracted_sentences = ["No source details were available for extraction."]

    confidence_level = "Low"

    if source_count >= 2:
        confidence_level = "Moderate"

    if source_count >= 3:
        confidence_level = "Moderate to High"

    if source_count == 1:
        confidence_reason = "Only one source was provided, so source comparison is limited."
    elif source_count >= 2:
        confidence_reason = "Multiple sources were provided, so basic comparison is possible. Human review is still required."
    else:
        confidence_reason = "No valid source text was provided, so confidence is low."

    selected_sections_text = format_selected_outputs(selected_outputs)
    selected_sections = [
        line.split(". ", 1)[1]
        for line in selected_sections_text.splitlines()
        if ". " in line
    ]

    report_lines = [
        "# TrendLens AI Report",
        "",
        "Draft generated using local fallback mode.",
        "",
        f"Fallback reason: {fallback_reason}",
        "",
        f"Target audience: {user_role}",
        f"Task type: {task_type}",
        f"Model route: {model_route}",
        f"Report purpose: {report_purpose}",
        f"Output depth: {output_depth}",
        "",
    ]

    for section in selected_sections:
        section_lower = section.lower()

        if "source overview" in section_lower:
            report_lines.extend(["## Source Overview", source_overview, ""])

        elif "raw tracker" in section_lower:
            report_lines.extend(
                [
                    "## Raw Tracker Entry",
                    "Event: Requires human review based on the provided public source text.",
                    f"Source count: {source_count}",
                    f"Audience: {user_role}",
                    f"Purpose: {report_purpose}",
                    "Status: Draft entry generated for review.",
                    "",
                ]
            )

        elif "bluf" in section_lower or "bottom line" in section_lower:
            report_lines.extend(
                [
                    "## BLUF",
                    "The provided public source text describes a developing or reviewable event that requires source validation, confidence assessment, and follow up questions before use.",
                    "",
                ]
            )

        elif "executive summary" in section_lower:
            report_lines.extend(
                [
                    "## Executive Summary",
                    "TrendLens AI organized the provided public source text into a draft situational awareness product. The source details should be reviewed by a human user before being used for decisions or briefings.",
                    "",
                ]
            )

        elif "5 ws" in section_lower or "key facts" in section_lower:
            report_lines.append("## Key Facts")

            for sentence in extracted_sentences[:8]:
                report_lines.append(f"1. {sentence}")

            report_lines.append("")

        elif "timeline" in section_lower:
            report_lines.extend(
                [
                    "## Timeline",
                    "A complete timeline requires additional source details or explicit dates and times from the user provided text.",
                    "",
                ]
            )

        elif "trend" in section_lower or "indicator" in section_lower or "pattern" in section_lower:
            report_lines.extend(
                [
                    "## Trend and Pattern Analysis",
                    "Trend analysis requires comparison across source text, prior reports, or updated information. The monitoring workflow can support this by comparing old and new source text.",
                    "",
                ]
            )

        elif "risk" in section_lower or "concern" in section_lower:
            report_lines.extend(
                [
                    "## Risks and Concerns",
                    "Potential risks depend on the event type, source reliability, confirmed impacts, and missing details. Human review should confirm whether public safety, infrastructure, operational, or information risks are present.",
                    "",
                ]
            )

        elif "second" in section_lower:
            report_lines.extend(
                [
                    "## Second Order Effects",
                    "Possible second order effects may include public confusion, resource coordination issues, operational delays, or increased information needs.",
                    "",
                ]
            )

        elif "third" in section_lower:
            report_lines.extend(
                [
                    "## Third Order Effects",
                    "Possible third order effects may include policy attention, longer term community impact, operational adjustments, or changes in public trust depending on the event.",
                    "",
                ]
            )

        elif "source comparison" in section_lower or "reliability" in section_lower:
            report_lines.extend(
                [
                    "## Source Comparison and Reliability Notes",
                    "Source comparison is limited in fallback mode. The user should review whether the sources agree on location, timeline, impact, official statements, and public safety guidance.",
                    "",
                ]
            )

        elif "confidence" in section_lower:
            report_lines.extend(
                [
                    "## Confidence Assessment",
                    f"Confidence level: {confidence_level}",
                    confidence_reason,
                    "",
                ]
            )

        elif "follow" in section_lower or "rfi" in section_lower or "collection gap" in section_lower:
            report_lines.extend(
                [
                    "## Follow Up Questions / RFIs",
                    "1. What details are confirmed by official public sources?",
                    "2. What details are still unconfirmed or missing?",
                    "3. Has the event location, timeline, impact, or public guidance changed?",
                    "4. Are there contradictions between public sources?",
                    "5. What information would change the confidence assessment?",
                    "",
                ]
            )

        elif "forty" in section_lower or "45" in section_lower:
            report_lines.extend(
                [
                    "## Forty Five Second Brief",
                    "TrendLens AI reviewed the provided public source text and generated a draft situational awareness product. The main value is the structured organization of known information, source gaps, confidence, and follow up questions. The report should be reviewed before use.",
                    "",
                ]
            )

        else:
            report_lines.extend(
                [
                    f"## {section}",
                    "This selected section requires additional source review or model output.",
                    "",
                ]
            )

    if custom_output_request:
        report_lines.extend(
            [
                "## Custom Instructions Noted",
                custom_output_request,
                "",
            ]
        )

    report_lines.extend(
        [
            "## Human Review Note",
            "This report is a draft for human review and should not be treated as an official product.",
        ]
    )

    return "\n".join(report_lines)


def generate_trendlens_report(
    sources: list[dict] = None,
    user_role: str = "Intelligence Analyst",
    report_purpose: str = "",
    selected_outputs: Optional[Union[dict, list[str]]] = None,
    custom_output_request: str = "",
    target_audience: str = None,
    selected_sections: Optional[list[str]] = None,
    custom_instructions: str = None,
    task_type: str = "Generate situational awareness report",
    output_depth: str = "Standard",
    model_route: str = "",
    model_name: str = "",
    **kwargs,
) -> str:
    ensure_project_folders()

    if target_audience:
        user_role = target_audience

    if selected_sections is not None:
        selected_outputs = selected_sections

    if custom_instructions is not None:
        custom_output_request = custom_instructions

    if not model_route:
        model_route = route_task(user_role, task_type)

    cleaned_sources = clean_sources(sources)

    if not cleaned_sources:
        return build_fallback_report(
            sources=[],
            user_role=user_role,
            report_purpose=report_purpose,
            selected_outputs=selected_outputs,
            custom_output_request=custom_output_request,
            task_type=task_type,
            output_depth=output_depth,
            model_route=model_route,
            fallback_reason="No valid source text was provided.",
        )

    system_prompt = build_system_prompt(
        user_role=user_role,
        task_type=task_type,
        model_route=model_route,
    )

    user_prompt = build_report_prompt(
        sources=cleaned_sources,
        user_role=user_role,
        report_purpose=report_purpose,
        selected_outputs=selected_outputs,
        custom_output_request=custom_output_request,
        task_type=task_type,
        output_depth=output_depth,
        model_route=model_route,
    )

    try:
        report = call_openai_model(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model_name=model_name,
        )

        if report:
            return report

    except Exception as error:
        return build_fallback_report(
            sources=cleaned_sources,
            user_role=user_role,
            report_purpose=report_purpose,
            selected_outputs=selected_outputs,
            custom_output_request=custom_output_request,
            task_type=task_type,
            output_depth=output_depth,
            model_route=model_route,
            fallback_reason=str(error),
        )

    return build_fallback_report(
        sources=cleaned_sources,
        user_role=user_role,
        report_purpose=report_purpose,
        selected_outputs=selected_outputs,
        custom_output_request=custom_output_request,
        task_type=task_type,
        output_depth=output_depth,
        model_route=model_route,
        fallback_reason="The model did not return a report.",
    )


def get_agent_workflow_summary(sources: list[dict]) -> str:
    cleaned_sources = clean_sources(sources)
    source_count = len(cleaned_sources)

    source_type_lines = []

    for index, source in enumerate(cleaned_sources, start=1):
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

9. Model Routing
Selected a route based on the user role and task type.

10. Report Generation
Generated one customized situational awareness report based on the selected role, report purpose, and requested output sections.

11. Session Memory
Stored the latest report and workflow summary in the current Streamlit session.

12. Feedback Logging
Allows the user to save feedback for later evaluation and improvement.

13. Monitoring Support
Supports the Project 2 monitoring workflow by preserving structured source text and report outputs for future comparison.
"""


def save_report(report_text: str, metadata: Optional[dict] = None) -> str:
    ensure_project_folders()

    if metadata is None:
        metadata = {}

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audience = safe_filename(metadata.get("target_audience", "audience"))
    task_type = safe_filename(metadata.get("task_type", "report"))

    file_path = OUTPUTS_DIR / f"trendlens_{audience}_{task_type}_{timestamp}.md"

    front_matter = {
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "metadata": metadata,
    }

    content = [
        "---",
        json.dumps(front_matter, indent=4),
        "---",
        "",
        str(report_text).strip(),
        "",
    ]

    file_path.write_text("\n".join(content), encoding="utf-8")

    save_report_index(file_path, metadata)

    return str(file_path)


def save_report_index(file_path: Path, metadata: Optional[dict] = None) -> str:
    ensure_project_folders()

    if metadata is None:
        metadata = {}

    index_file = OUTPUTS_DIR / "report_index.csv"
    file_exists = index_file.exists()

    fieldnames = [
        "saved_at",
        "file_path",
        "target_audience",
        "task_type",
        "report_purpose",
        "model_route",
        "valid_source_count",
    ]

    row = {
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file_path": str(file_path),
        "target_audience": metadata.get("target_audience", ""),
        "task_type": metadata.get("task_type", ""),
        "report_purpose": metadata.get("report_purpose", ""),
        "model_route": metadata.get("model_route", ""),
        "valid_source_count": metadata.get("valid_source_count", ""),
    }

    with open(index_file, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    return str(index_file)


def save_feedback(
    feedback_text: str = "",
    rating: Optional[int] = None,
    metadata: Optional[dict] = None,
    feedback: str = "",
    notes: str = "",
) -> str:
    ensure_project_folders()

    if metadata is None:
        metadata = {}

    if not feedback_text and feedback:
        feedback_text = feedback

    if notes and not metadata.get("notes"):
        metadata["notes"] = notes

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_path = OUTPUTS_DIR / "feedback_log.csv"
    json_feedback_path = DATA_DIR / f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    new_file = not feedback_path.exists()

    fieldnames = [
        "timestamp",
        "rating",
        "feedback_text",
        "notes",
        "target_audience",
        "task_type",
        "model_route",
        "latest_report_path",
    ]

    row = {
        "timestamp": timestamp,
        "rating": rating if rating is not None else "",
        "feedback_text": clean_source_text(feedback_text),
        "notes": metadata.get("notes", ""),
        "target_audience": metadata.get("target_audience", ""),
        "task_type": metadata.get("task_type", ""),
        "model_route": metadata.get("model_route", ""),
        "latest_report_path": metadata.get("latest_report_path", ""),
    }

    with feedback_path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if new_file:
            writer.writeheader()

        writer.writerow(row)

    json_feedback = {
        "timestamp": timestamp,
        "rating": row["rating"],
        "feedback_text": row["feedback_text"],
        "metadata": metadata,
    }

    json_feedback_path.write_text(
        json.dumps(json_feedback, indent=4),
        encoding="utf-8",
    )

    return str(feedback_path)


def create_evaluation_record(
    test_name: str,
    input_type: str,
    role: str,
    purpose: str,
    expected_result: str,
    actual_result: str,
    result_status: str,
    notes: str,
) -> str:
    ensure_project_folders()

    eval_file = TESTS_DIR / "eval_results.md"

    entry = f"""
## {test_name}

Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Input type: {input_type}

Role: {role}

Purpose: {purpose}

Expected result: {expected_result}

Actual result: {actual_result}

Result: {result_status}

Notes: {notes}
"""

    with open(eval_file, "a", encoding="utf-8") as file:
        file.write(entry)

    return str(eval_file)


if __name__ == "__main__":
    sample_sources = [
        {
            "source_number": 1,
            "type": "Public safety alert",
            "label": "City alert",
            "url": "",
            "text": (
                "City officials reported a chemical spill near an industrial facility. "
                "Roads near the facility were closed while crews assessed the scene."
            ),
        },
        {
            "source_number": 2,
            "type": "News article",
            "label": "Local news article",
            "url": "",
            "text": (
                "Fire officials confirmed that nearby businesses were evacuated as a precaution. "
                "The county emergency management office told the public to avoid the area."
            ),
        },
    ]

    sample_report = generate_trendlens_report(
        sources=sample_sources,
        target_audience="Intelligence Analyst",
        report_purpose="Compare public reporting and create a situational awareness update.",
        selected_sections=[
            "Source Overview",
            "BLUF",
            "Executive Summary",
            "Source Comparison and Reliability Notes",
            "Confidence Assessment",
            "Recommended Follow Up Questions",
        ],
        custom_instructions="Use active voice and avoid unsupported assumptions.",
        task_type="Generate situational awareness report",
        output_depth="Standard",
        model_route="Intelligence Analyst Route",
    )

    print(sample_report)