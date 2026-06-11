import json
import os
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image, UnidentifiedImageError

from auth import render_auth_gate
from security_utils import validate_public_sources
from ui_components import render_welcome_video

from trend_tools import save_feedback, save_report


try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
    OPENAI_IMPORT_ERROR = ""
except Exception as error:
    OpenAI = None
    OPENAI_AVAILABLE = False
    OPENAI_IMPORT_ERROR = str(error)


try:
    from monitoring import (
        compare_source_changes,
        load_monitored_topics,
        save_monitored_topic,
    )

    MONITORING_AVAILABLE = True
    MONITORING_IMPORT_ERROR = ""
except Exception as error:
    MONITORING_AVAILABLE = False
    MONITORING_IMPORT_ERROR = str(error)


APP_NAME = "TrendLens AI"

OUTPUTS_DIR = Path("Outputs")
MONITORING_DIR = Path("Monitoring")
ASSETS_DIR = Path("assets")
TESTS_DIR = Path("Tests")

ICON_PATH = ASSETS_DIR / "trendlens-icon.png"
BANNER_PATH = ASSETS_DIR / "trendlens-banner.png"

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# P3 update:
# The router uses an LLM tool call to choose the route. The generation step then
# dispatches to the model assigned to that route. These can be changed in
# Streamlit secrets or environment variables without editing code.
ROUTER_MODEL = os.getenv("OPENAI_ROUTER_MODEL", "gpt-4o-mini")
FAST_MODEL = os.getenv("OPENAI_FAST_MODEL", "gpt-4o-mini")
DEEP_ANALYSIS_MODEL = os.getenv("OPENAI_DEEP_ANALYSIS_MODEL", "gpt-4o")
SOURCE_COMPARISON_MODEL = os.getenv("OPENAI_SOURCE_COMPARISON_MODEL", "gpt-4o")
MONITORING_MODEL = os.getenv("OPENAI_MONITORING_MODEL", "gpt-4o-mini")
EXECUTIVE_BRIEF_MODEL = os.getenv("OPENAI_EXECUTIVE_BRIEF_MODEL", "gpt-4o-mini")
FALLBACK_REPORT_MODEL = os.getenv("OPENAI_FALLBACK_REPORT_MODEL", "gpt-4o-mini")


ANALYZE_PUBLIC_SOURCES_TOOL = {
    "type": "function",
    "function": {
        "name": "analyze_public_sources",
        "description": (
            "Analyze user provided public source text before the final situational "
            "awareness report is written. Compare sources, identify source supported "
            "facts, possible conflicts, information gaps, confidence level, and possible "
            "second and third order effects."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sources": {
                    "type": "array",
                    "description": "Public source records pasted by the user.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "source_number": {"type": "integer"},
                            "type": {"type": "string"},
                            "label": {"type": "string"},
                            "url": {"type": "string"},
                            "text": {"type": "string"},
                        },
                        "required": ["source_number", "type", "label", "text"],
                        "additionalProperties": True,
                    },
                },
                "target_audience": {
                    "type": "string",
                    "description": "Audience selected by the user.",
                },
                "report_purpose": {
                    "type": "string",
                    "description": "Purpose of the report entered by the user.",
                },
                "task_type": {
                    "type": "string",
                    "description": "Task type selected by the user.",
                },
                "selected_sections": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Report sections selected by the user.",
                },
            },
            "required": [
                "sources",
                "target_audience",
                "report_purpose",
                "task_type",
                "selected_sections",
            ],
            "additionalProperties": False,
        },
    },
}



SELECT_TRENDLENS_ROUTE_TOOL = {
    "type": "function",
    "function": {
        "name": "select_trendlens_route",
        "description": (
            "Choose the best TrendLens AI analysis route and generation model based "
            "on the user's audience, task type, purpose, selected sections, and pasted "
            "source text. This is the P3 LLM-based routing decision."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "route_name": {
                    "type": "string",
                    "enum": [
                        "fast_trend_summary",
                        "deep_risk_analysis",
                        "source_comparison",
                        "monitoring_update",
                        "executive_brief",
                        "fallback_report",
                    ],
                    "description": "The route selected for this request.",
                },
                "reason": {
                    "type": "string",
                    "description": "Brief reason explaining why this route fits the input.",
                },
                "confidence": {
                    "type": "string",
                    "enum": ["Low", "Moderate", "High"],
                    "description": "Confidence in the routing choice.",
                },
                "evidence_from_input": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Short cues from the user's selections or source text that support the route.",
                },
                "user_visible_summary": {
                    "type": "string",
                    "description": "One sentence summary suitable to show in the app trace.",
                },
            },
            "required": [
                "route_name",
                "reason",
                "confidence",
                "evidence_from_input",
                "user_visible_summary",
            ],
            "additionalProperties": False,
        },
    },
}


def safe_load_image(image_path):
    """
    Safely loads an image file so the app does not crash if an asset is missing,
    empty, corrupted, or not a real image file.
    """
    try:
        if image_path.exists() and image_path.stat().st_size > 0:
            return Image.open(image_path)
    except (UnidentifiedImageError, OSError, ValueError):
        return None

    return None


page_icon_image = safe_load_image(ICON_PATH)
banner_image = safe_load_image(BANNER_PATH)

page_icon = page_icon_image if page_icon_image is not None else "🔎"


st.set_page_config(
    page_title="TrendLens AI",
    page_icon=page_icon,
    layout="wide",
)

render_auth_gate()

# Small settings panel in the sidebar (non-breaking defaults)
try:
    with st.sidebar.expander("Settings", expanded=False):
        show_welcome = st.checkbox(
            "Show welcome video",
            value=st.session_state.get("show_welcome_video", True),
            key="show_welcome_video",
        )

        show_workflow = st.checkbox(
            "Show workflow preview",
            value=st.session_state.get("show_workflow_preview", True),
            key="show_workflow_preview",
        )

        st.caption("Display options only. No authentication changes are made here.")
except Exception:
    # Ignore sidebar issues in non-Streamlit contexts
    pass


def initialize_session_state():
    if "latest_report" not in st.session_state:
        st.session_state.latest_report = ""

    if "latest_report_path" not in st.session_state:
        st.session_state.latest_report_path = ""

    if "latest_metadata" not in st.session_state:
        st.session_state.latest_metadata = {}

    if "latest_tool_trace" not in st.session_state:
        st.session_state.latest_tool_trace = {}

    if "latest_generation_mode" not in st.session_state:
        st.session_state.latest_generation_mode = ""

    if "latest_routing_decision" not in st.session_state:
        st.session_state.latest_routing_decision = {}

    if "feedback_saved" not in st.session_state:
        st.session_state.feedback_saved = False

    if "eval_saved" not in st.session_state:
        st.session_state.eval_saved = False

    if "selected_sections" not in st.session_state:
        st.session_state.selected_sections = [
            "Source Overview",
            "Bottom Line Up Front",
            "Executive Summary",
            "So What / Why This Matters",
            "Source Comparison and Reliability Notes",
            "Confidence Assessment",
            "Follow Up Questions / RFIs",
            "Forty Five Second Brief",
        ]
    if "show_welcome_video" not in st.session_state:
        st.session_state.show_welcome_video = True

    if "show_workflow_preview" not in st.session_state:
        st.session_state.show_workflow_preview = True


def ensure_project_folders():
    OUTPUTS_DIR.mkdir(exist_ok=True)
    MONITORING_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)
    TESTS_DIR.mkdir(exist_ok=True)


def get_openai_api_key():
    """
    Reads the OpenAI API key from Streamlit secrets first, then from the local
    environment. Never hard code the API key in app.py.
    """
    try:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        if api_key:
            return api_key
    except Exception:
        pass

    return os.getenv("OPENAI_API_KEY", "")


def get_openai_client():
    if not OPENAI_AVAILABLE:
        raise RuntimeError(
            f"The openai package is not available. Install it with: pip install openai. Details: {OPENAI_IMPORT_ERROR}"
        )

    api_key = get_openai_api_key()

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to Streamlit secrets or set it as a local environment variable."
        )

    return OpenAI(api_key=api_key)



def get_route_catalog():
    """
    Central catalog for true route-to-model dispatch.

    The LLM router chooses one route_name. The app then uses this catalog to
    select the generation model and route instructions. Change the environment
    variables above if a different model name is needed for your account.
    """
    return {
        "fast_trend_summary": {
            "display_name": "Fast Trend Summary Route",
            "selected_model": FAST_MODEL,
            "model_key": "OPENAI_FAST_MODEL",
            "route_instructions": (
                "Generate a concise trend summary with a clear BLUF, key facts, "
                "confidence language, and only the most important follow-up questions."
            ),
        },
        "deep_risk_analysis": {
            "display_name": "Deep Risk Analysis Route",
            "selected_model": DEEP_ANALYSIS_MODEL,
            "model_key": "OPENAI_DEEP_ANALYSIS_MODEL",
            "route_instructions": (
                "Generate a deeper risk-focused report. Emphasize risk, impact, "
                "second and third order effects, assumptions, confidence, and RFIs."
            ),
        },
        "source_comparison": {
            "display_name": "Source Comparison Route",
            "selected_model": SOURCE_COMPARISON_MODEL,
            "model_key": "OPENAI_SOURCE_COMPARISON_MODEL",
            "route_instructions": (
                "Generate a source comparison report. Emphasize agreement, disagreement, "
                "source limits, possible conflicts, and what needs verification."
            ),
        },
        "monitoring_update": {
            "display_name": "Monitoring Update Route",
            "selected_model": MONITORING_MODEL,
            "model_key": "OPENAI_MONITORING_MODEL",
            "route_instructions": (
                "Generate an update-style report. Emphasize what changed, why it matters, "
                "whether the change appears meaningful, and what should be monitored next."
            ),
        },
        "executive_brief": {
            "display_name": "Executive Brief Route",
            "selected_model": EXECUTIVE_BRIEF_MODEL,
            "model_key": "OPENAI_EXECUTIVE_BRIEF_MODEL",
            "route_instructions": (
                "Generate a short executive-ready briefing with BLUF, key judgments, "
                "decision relevance, confidence, and recommended next questions."
            ),
        },
        "fallback_report": {
            "display_name": "Fallback Report Route",
            "selected_model": FALLBACK_REPORT_MODEL,
            "model_key": "OPENAI_FALLBACK_REPORT_MODEL",
            "route_instructions": (
                "Generate a safe fallback-style report. Keep claims limited, flag missing "
                "information, and avoid unsupported assumptions."
            ),
        },
    }


def route_prompt_behavior(target_audience, task_type):
    """
    Legacy helper kept for transparency and backward compatibility.

    Earlier versions used this Python-only route label. P3 now uses
    route_model_behavior_with_llm(), which makes the actual routing decision
    through an LLM tool call and dispatches to a selected generation model.
    """
    audience = target_audience.lower()
    task = task_type.lower()

    if "monitor" in task or "update" in task:
        return {
            "route_name": "Instruction Path: Monitoring Update",
            "route_explanation": (
                "Legacy Python prompt hint. Actual P3 routing is selected by the LLM router after Generate is clicked."
            ),
        }

    if "intelligence" in audience:
        return {
            "route_name": "Instruction Path: Intelligence Analyst",
            "route_explanation": (
                "Legacy Python prompt hint. Actual P3 routing is selected by the LLM router after Generate is clicked."
            ),
        }

    if "emergency" in audience:
        return {
            "route_name": "Instruction Path: Emergency Response",
            "route_explanation": (
                "Legacy Python prompt hint. Actual P3 routing is selected by the LLM router after Generate is clicked."
            ),
        }

    if "public" in audience:
        return {
            "route_name": "Instruction Path: Public Audience",
            "route_explanation": (
                "Legacy Python prompt hint. Actual P3 routing is selected by the LLM router after Generate is clicked."
            ),
        }

    if "journalist" in audience or "researcher" in audience:
        return {
            "route_name": "Instruction Path: Research and Journalism",
            "route_explanation": (
                "Legacy Python prompt hint. Actual P3 routing is selected by the LLM router after Generate is clicked."
            ),
        }

    if "security" in audience:
        return {
            "route_name": "Instruction Path: Security Professional",
            "route_explanation": (
                "Legacy Python prompt hint. Actual P3 routing is selected by the LLM router after Generate is clicked."
            ),
        }

    return {
        "route_name": "Instruction Path: General Situational Awareness",
        "route_explanation": (
            "Legacy Python prompt hint. Actual P3 routing is selected by the LLM router after Generate is clicked."
        ),
    }


def truncate_for_router(text, max_chars=900):
    cleaned = clean_text(text)

    if len(cleaned) <= max_chars:
        return cleaned

    return cleaned[:max_chars] + "..."


def build_router_source_summaries(sources):
    summaries = []

    for source in sources:
        summaries.append(
            {
                "source_number": source.get("source_number", len(summaries) + 1),
                "type": source.get("type", "Not specified"),
                "label": source.get("label", "Source"),
                "url_present": bool(source.get("url", "")),
                "text_preview": truncate_for_router(source.get("text", ""), max_chars=900),
            }
        )

    return summaries


def normalize_route_name(route_name):
    route_catalog = get_route_catalog()
    cleaned_route = str(route_name or "").strip().lower()

    if cleaned_route in route_catalog:
        return cleaned_route

    # Safe default if the router returns an unexpected value.
    return "fast_trend_summary"


def route_model_behavior_with_llm(
    sources,
    target_audience,
    report_purpose,
    selected_sections,
    task_type,
    output_depth,
):
    """
    P3 routing upgrade.

    This replaces the Python-only routing decision with an LLM tool call. The
    model must call select_trendlens_route. The app then dispatches the report
    generation step to the model assigned to that route.
    """
    client = get_openai_client()
    route_catalog = get_route_catalog()

    route_catalog_for_prompt = {
        route_name: {
            "display_name": route_data["display_name"],
            "generation_model": route_data["selected_model"],
            "model_env_key": route_data["model_key"],
            "best_for": route_data["route_instructions"],
        }
        for route_name, route_data in route_catalog.items()
    }

    router_payload = {
        "target_audience": target_audience,
        "report_purpose": report_purpose,
        "task_type": task_type,
        "output_depth": output_depth,
        "selected_sections": selected_sections,
        "source_count": len(sources),
        "source_summaries": build_router_source_summaries(sources),
        "available_routes": route_catalog_for_prompt,
    }

    system_message = """
You are the TrendLens AI routing model.

Your job is not to write the final report. Your job is to choose the best route
for the request and call the select_trendlens_route tool exactly once.

Choose based on the user's task type, target audience, selected sections, report
purpose, and source text previews.

Route selection guidance:
- fast_trend_summary: quick, standard, or general situational awareness requests.
- deep_risk_analysis: risk, threat, security, consequences, impacts, or complex events.
- source_comparison: comparing multiple sources, conflicting claims, reliability, or attribution.
- monitoring_update: monitoring, update, changed source text, anomaly, or ongoing event tracking.
- executive_brief: leadership, decision-maker, executive briefing, short commander-style brief.
- fallback_report: limited information, weak inputs, unclear topic, or when a cautious report is safest.

Return only the tool call. Do not write normal text.
"""

    user_message = f"""
Select the best TrendLens AI route for this request.

Routing payload:
{json.dumps(router_payload, indent=2)}
"""

    response = client.chat.completions.create(
        model=ROUTER_MODEL,
        messages=[
            {"role": "system", "content": system_message.strip()},
            {"role": "user", "content": user_message.strip()},
        ],
        tools=[SELECT_TRENDLENS_ROUTE_TOOL],
        tool_choice={
            "type": "function",
            "function": {"name": "select_trendlens_route"},
        },
        temperature=0,
    )

    message = response.choices[0].message
    tool_calls = message.tool_calls or []

    if not tool_calls:
        raise RuntimeError(
            "The router model did not call select_trendlens_route. Routing cannot continue."
        )

    route_call = tool_calls[0]

    try:
        route_args = json.loads(route_call.function.arguments or "{}")
    except json.JSONDecodeError:
        route_args = {}

    route_name = normalize_route_name(route_args.get("route_name", "fast_trend_summary"))
    route_data = route_catalog[route_name]

    routing_decision = {
        "routing_type": "llm tool based model routing",
        "router_model": ROUTER_MODEL,
        "router_tool_name": "select_trendlens_route",
        "router_tool_requested": True,
        "route_name": route_name,
        "route_display_name": route_data["display_name"],
        "selected_model": route_data["selected_model"],
        "model_key": route_data["model_key"],
        "route_instructions": route_data["route_instructions"],
        "reason": clean_text(route_args.get("reason", "")),
        "confidence": route_args.get("confidence", "Moderate"),
        "evidence_from_input": route_args.get("evidence_from_input", []),
        "user_visible_summary": clean_text(route_args.get("user_visible_summary", "")),
        "available_routes": {
            name: data["selected_model"] for name, data in route_catalog.items()
        },
    }

    if not routing_decision["reason"]:
        routing_decision["reason"] = (
            "The LLM router selected this route based on the user's audience, task type, purpose, and source text."
        )

    if not routing_decision["user_visible_summary"]:
        routing_decision["user_visible_summary"] = (
            f"Selected {route_data['display_name']} using {route_data['selected_model']}."
        )

    return routing_decision

def build_source_payload(source_1, source_2, source_3):
    sources = []

    for index, source in enumerate([source_1, source_2, source_3], start=1):
        source_text = source.get("text", "").strip()

        if source_text:
            sources.append(
                {
                    "source_number": index,
                    "type": source.get("type", "Not specified"),
                    "label": source.get("label", f"Source {index}"),
                    "url": source.get("url", ""),
                    "text": source_text,
                }
            )

    return sources



def build_metadata(
    target_audience,
    report_purpose,
    task_type,
    output_depth,
    selected_sections,
    sources,
    routing_decision,
):
    return {
        "app_name": APP_NAME,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target_audience": target_audience,
        "report_purpose": report_purpose,
        "task_type": task_type,
        "output_depth": output_depth,
        "selected_sections": selected_sections,
        "valid_source_count": len(sources),
        "routing_type": routing_decision.get(
            "routing_type", "llm tool based model routing"
        ),
        "router_model": routing_decision.get("router_model", ROUTER_MODEL),
        "router_tool_name": routing_decision.get(
            "router_tool_name", "select_trendlens_route"
        ),
        "router_tool_requested": routing_decision.get(
            "router_tool_requested", False
        ),
        "llm_route": routing_decision.get("route_name", ""),
        "route_display_name": routing_decision.get("route_display_name", ""),
        "route_reason": routing_decision.get("reason", ""),
        "route_confidence": routing_decision.get("confidence", ""),
        "route_evidence": routing_decision.get("evidence_from_input", []),
        "generation_model": routing_decision.get("selected_model", DEFAULT_MODEL),
        "model_name": routing_decision.get("selected_model", DEFAULT_MODEL),
    }

def clean_text(text):
    return re.sub(r"\s+", " ", str(text or "")).strip()


def extract_keywords(text, limit=12):
    stop_words = {
        "about",
        "after",
        "again",
        "also",
        "and",
        "are",
        "because",
        "been",
        "before",
        "being",
        "could",
        "during",
        "each",
        "from",
        "have",
        "into",
        "more",
        "most",
        "not",
        "only",
        "other",
        "over",
        "public",
        "said",
        "same",
        "source",
        "that",
        "the",
        "their",
        "there",
        "these",
        "they",
        "this",
        "through",
        "under",
        "updated",
        "were",
        "what",
        "when",
        "where",
        "which",
        "while",
        "with",
        "would",
    }

    words = re.findall(r"\b[A-Za-z][A-Za-z0-9]{3,}\b", text.lower())
    filtered_words = [word for word in words if word not in stop_words]

    return [word for word, _count in Counter(filtered_words).most_common(limit)]


def summarize_source(source):
    source_text = clean_text(source.get("text", ""))
    words = source_text.split()

    if not words:
        return "No usable source text provided."

    preview = " ".join(words[:55])

    if len(words) > 55:
        preview += "..."

    return preview


def find_possible_review_flags(sources):
    """
    Flags items that should be checked by a human reviewer. This does not claim
    that a conflict exists. It identifies details that may need verification.
    """
    numbers_by_source = {}
    dates_by_source = {}
    locations_by_source = {}

    location_pattern = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}\b")

    excluded_locations = {
        "The",
        "This",
        "That",
        "Source",
        "Public",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    }

    for source in sources:
        label = source.get("label", f"Source {source.get('source_number', '')}")
        text = clean_text(source.get("text", ""))

        numbers = sorted(set(re.findall(r"\b\d{1,4}\b", text)))
        dates = sorted(
            set(
                re.findall(
                    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b",
                    text,
                    flags=re.IGNORECASE,
                )
            )
        )
        locations = sorted(
            {
                match.group(0)
                for match in location_pattern.finditer(text)
                if match.group(0) not in excluded_locations
            }
        )

        if numbers:
            numbers_by_source[label] = numbers[:12]

        if dates:
            dates_by_source[label] = dates[:12]

        if locations:
            locations_by_source[label] = locations[:12]

    review_flags = []

    if len(numbers_by_source) > 1:
        review_flags.append(
            "Multiple sources contain numeric details. Review counts, times, quantities, distances, or costs for consistency."
        )

    if len(dates_by_source) > 1:
        review_flags.append(
            "Multiple sources contain date or time details. Review the timeline for consistency."
        )

    if len(locations_by_source) > 1:
        review_flags.append(
            "Multiple sources contain location references. Review whether locations refer to the same event area or different impact areas."
        )

    if not review_flags:
        review_flags.append(
            "No obvious numeric, date, or location review flag was detected. Human review is still required."
        )

    return {
        "review_flags": review_flags,
        "numbers_by_source": numbers_by_source,
        "dates_by_source": dates_by_source,
        "locations_by_source": locations_by_source,
    }


def estimate_confidence(source_count):
    if source_count >= 3:
        return "Moderate"

    if source_count == 2:
        return "Low to moderate"

    return "Low"


def analyze_public_sources(
    sources,
    target_audience,
    report_purpose,
    task_type,
    selected_sections,
):
    """
    Real model callable application tool.

    The model receives a function schema for this tool. The model must request
    this function before the final report is written. The app executes this
    local Python function only after the model requests it.
    """
    usable_sources = []

    for source in sources:
        source_text = clean_text(source.get("text", ""))

        if not source_text:
            continue

        usable_sources.append(
            {
                "source_number": int(source.get("source_number", len(usable_sources) + 1)),
                "type": source.get("type", "Not specified"),
                "label": source.get("label", f"Source {len(usable_sources) + 1}"),
                "url": source.get("url", ""),
                "text": source_text,
            }
        )

    combined_text = " ".join(source["text"] for source in usable_sources)
    overall_keywords = extract_keywords(combined_text, limit=18)

    keyword_sets = [
        set(extract_keywords(source["text"], limit=20))
        for source in usable_sources
    ]

    if len(keyword_sets) >= 2:
        shared_keywords = sorted(set.intersection(*keyword_sets))[:12]
    elif keyword_sets:
        shared_keywords = sorted(keyword_sets[0])[:12]
    else:
        shared_keywords = []

    review_flags = find_possible_review_flags(usable_sources)
    confidence_level = estimate_confidence(len(usable_sources))

    source_previews = []

    for source in usable_sources:
        source_previews.append(
            {
                "source_number": source["source_number"],
                "type": source["type"],
                "label": source["label"],
                "url_present": bool(source.get("url")),
                "preview": summarize_source(source),
                "top_keywords": extract_keywords(source["text"], limit=8),
            }
        )

    likely_topic = "Public event requiring source comparison"

    if overall_keywords:
        likely_topic = "Public event involving " + ", ".join(overall_keywords[:6])

    return {
        "tool_name": "analyze_public_sources",
        "tool_executed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_count": len(usable_sources),
        "target_audience": target_audience,
        "report_purpose": report_purpose,
        "task_type": task_type,
        "selected_sections": selected_sections,
        "likely_topic": likely_topic,
        "source_previews": source_previews,
        "overall_keywords": overall_keywords,
        "shared_keywords": shared_keywords,
        "possible_conflicts_or_review_flags": review_flags,
        "information_gaps": [
            "Most current official confirmation.",
            "Exact timeline of what changed and when.",
            "Clarification of any conflicting counts, locations, or impact claims.",
            "Clear source attribution for key claims used in the final report.",
            "Updated public safety, operational, or community guidance if the event is still developing.",
        ],
        "possible_second_and_third_order_effects": [
            "Immediate effects may include public communication needs, resource coordination, or local operational disruption.",
            "Second order effects may include route changes, delayed services, resource strain, stakeholder concern, or increased reporting requirements.",
            "Third order effects may include policy review, reputational impact, supply chain concern, recovery planning, or long term community confidence issues.",
        ],
        "confidence_level": confidence_level,
        "analysis_limits": (
            "This tool only analyzes user pasted public or synthetic source text. "
            "It does not browse the web or independently verify facts."
        ),
    }



def build_tool_workflow_messages(
    sources,
    target_audience,
    report_purpose,
    selected_sections,
    custom_instructions,
    task_type,
    output_depth,
    routing_decision,
):
    source_package = {
        "sources": sources,
        "target_audience": target_audience,
        "report_purpose": report_purpose,
        "task_type": task_type,
        "selected_sections": selected_sections,
    }

    system_message = f"""
You are TrendLens AI, an agentic public event analysis assistant.

Required workflow:
1. Use the LLM-selected route below as the analysis behavior for this report.
2. Call the analyze_public_sources function before writing the final report.
3. Use the tool result as the grounding layer for source comparison, confidence, information gaps, and second and third order effects.
4. Do not claim that you verified facts outside the user provided source text.
5. Separate source supported details from possible implications.
6. Keep the tone appropriate for the selected audience.
7. Use only public or synthetic information.
8. Do not include classified, private, restricted, protected, or sensitive information.

LLM selected route:
{routing_decision.get("route_display_name", routing_decision.get("route_name", ""))}

Route instructions:
{routing_decision.get("route_instructions", "")}
"""

    user_message = f"""
Create a structured situational awareness report.

Target audience:
{target_audience}

Report purpose:
{report_purpose}

Task type:
{task_type}

Output depth:
{output_depth}

Routing type:
{routing_decision.get("routing_type", "llm tool based model routing")}

Router model:
{routing_decision.get("router_model", ROUTER_MODEL)}

Router tool:
{routing_decision.get("router_tool_name", "select_trendlens_route")}

LLM selected route:
{routing_decision.get("route_display_name", routing_decision.get("route_name", ""))}

Selected generation model:
{routing_decision.get("selected_model", DEFAULT_MODEL)}

Reason for route:
{routing_decision.get("reason", "")}

Route confidence:
{routing_decision.get("confidence", "")}

Selected report sections:
{", ".join(selected_sections)}

Optional custom instructions:
{custom_instructions if custom_instructions.strip() else "None provided."}

Public source package:
{json.dumps(source_package, indent=2)}

After the function tool returns its result, write the final report using the selected sections.
"""

    return [
        {"role": "system", "content": system_message.strip()},
        {"role": "user", "content": user_message.strip()},
    ]


def run_model_tool_workflow(
    sources,
    target_audience,
    report_purpose,
    selected_sections,
    custom_instructions,
    task_type,
    output_depth,
    routing_decision,
):
    """
    Strict model callable tool workflow.

    P3 update:
    1. The router model already selected a route through select_trendlens_route.
    2. This function dispatches report generation to the model assigned to that route.
    3. The selected generation model must call analyze_public_sources before writing.
    """
    client = get_openai_client()
    model_name = routing_decision.get("selected_model", DEFAULT_MODEL)

    messages = build_tool_workflow_messages(
        sources=sources,
        target_audience=target_audience,
        report_purpose=report_purpose,
        selected_sections=selected_sections,
        custom_instructions=custom_instructions,
        task_type=task_type,
        output_depth=output_depth,
        routing_decision=routing_decision,
    )

    first_response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=[ANALYZE_PUBLIC_SOURCES_TOOL],
        tool_choice={
            "type": "function",
            "function": {"name": "analyze_public_sources"},
        },
        temperature=0.2,
    )

    first_message = first_response.choices[0].message
    tool_calls = first_message.tool_calls or []

    if not tool_calls:
        raise RuntimeError(
            "The generation model did not request analyze_public_sources. The report was not generated because real model tool use is required."
        )

    messages.append(first_message.model_dump(exclude_none=True))

    tool_trace = {
        "generation_mode": "llm routed model callable tool workflow",
        "routing_type": routing_decision.get(
            "routing_type", "llm tool based model routing"
        ),
        "router_model": routing_decision.get("router_model", ROUTER_MODEL),
        "router_tool_name": routing_decision.get(
            "router_tool_name", "select_trendlens_route"
        ),
        "router_tool_requested": routing_decision.get(
            "router_tool_requested", False
        ),
        "llm_route": routing_decision.get("route_name", ""),
        "route_display_name": routing_decision.get("route_display_name", ""),
        "route_reason": routing_decision.get("reason", ""),
        "route_confidence": routing_decision.get("confidence", ""),
        "route_evidence": routing_decision.get("evidence_from_input", []),
        "generation_model": model_name,
        "tool_requested_by_model": False,
        "tool_name": "",
        "tool_result_summary": {},
        "workflow_steps": [
            "The app sent the request to the router model.",
            "The router model called select_trendlens_route.",
            "The app mapped the LLM route to a generation model.",
            "The app dispatched report generation to the selected model.",
            "The app provided a function schema to the generation model.",
            "The generation model requested analyze_public_sources.",
            "The app executed the Python function after the model requested it.",
            "The app returned the tool result to the model.",
            "The model generated the final report after receiving the tool result.",
        ],
    }

    for tool_call in tool_calls:
        tool_name = tool_call.function.name

        if tool_name != "analyze_public_sources":
            raise RuntimeError(f"Unexpected tool requested by model: {tool_name}")

        try:
            arguments = json.loads(tool_call.function.arguments or "{}")
        except json.JSONDecodeError:
            arguments = {}

        tool_result = analyze_public_sources(
            sources=arguments.get("sources", sources),
            target_audience=arguments.get("target_audience", target_audience),
            report_purpose=arguments.get("report_purpose", report_purpose),
            task_type=arguments.get("task_type", task_type),
            selected_sections=arguments.get("selected_sections", selected_sections),
        )

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result, indent=2),
            }
        )

        tool_trace["tool_requested_by_model"] = True
        tool_trace["tool_name"] = "analyze_public_sources"
        tool_trace["tool_result_summary"] = {
            "source_count": tool_result["source_count"],
            "likely_topic": tool_result["likely_topic"],
            "confidence_level": tool_result["confidence_level"],
            "review_flags": tool_result["possible_conflicts_or_review_flags"]["review_flags"],
        }

    final_response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.3,
    )

    final_report = final_response.choices[0].message.content or ""

    if not final_report.strip():
        raise RuntimeError("The model returned an empty report.")

    return final_report, tool_trace

def call_save_report(report_text, metadata):
    try:
        return save_report(report_text=report_text, metadata=metadata)
    except TypeError:
        pass

    try:
        return save_report(report_text, metadata)
    except TypeError:
        pass

    return save_report(report_text)


def call_save_feedback(feedback_text, rating, metadata):
    try:
        return save_feedback(
            feedback_text=feedback_text,
            rating=rating,
            metadata=metadata,
        )
    except TypeError:
        pass

    try:
        return save_feedback(feedback_text, rating, metadata)
    except TypeError:
        pass

    try:
        return save_feedback(feedback_text, rating)
    except TypeError:
        pass

    return save_feedback(feedback_text)



def save_eval_record(expected_output, actual_output, metadata, tool_trace):
    TESTS_DIR.mkdir(exist_ok=True)
    eval_path = TESTS_DIR / "eval_results.md"

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    record = f"""
## Evaluation Record

Date:
{created_at}

Test purpose:
Confirm TrendLens AI uses LLM tool-based routing and then uses a real model callable tool before generating a structured situational awareness report.

Expected output:
{expected_output.strip()}

Actual output:
{actual_output.strip()}

Generation mode:
{metadata.get("generation_mode", "")}

Routing type:
{metadata.get("routing_type", "")}

Router model:
{metadata.get("router_model", "")}

Router tool:
{metadata.get("router_tool_name", "")}

LLM route selected:
{metadata.get("route_display_name", metadata.get("llm_route", ""))}

Route reason:
{metadata.get("route_reason", "")}

Selected generation model:
{metadata.get("generation_model", metadata.get("model_name", ""))}

Analysis tool used:
{metadata.get("model_tool_used", "")}

Tool trace summary:
~~~json
{json.dumps(tool_trace, indent=2)}
~~~

Result:
The P3 workflow is successful if the trace shows that the router model requested select_trendlens_route, the app dispatched to the selected generation model, and the generation model requested analyze_public_sources before the final report was written.

---
"""

    with eval_path.open("a", encoding="utf-8") as file:
        file.write(record)

    return eval_path

def render_header():
    if banner_image is not None:
        st.image(banner_image, width="stretch")
    else:
        header_left, header_right = st.columns([1, 8])

        with header_left:
            if page_icon_image is not None:
                st.image(page_icon_image, width=90)
            else:
                st.markdown("## 🔎")

        with header_right:
            st.title("TrendLens AI")
            st.caption("Agentic public event analysis and situational awareness reporting assistant")

    st.markdown(
        """
TrendLens AI helps transform multiple public information sources into one structured situational awareness product.

For this working draft, paste two or three public article excerpts, alerts, reports, updates, or event descriptions. The system uses a real model callable function tool to analyze the sources before the final report is written.
"""
    )



def render_agent_workflow_panel(valid_source_count, selected_sections):
    with st.expander("Agent workflow preview", expanded=True):
        st.markdown(
            """
This panel shows the actual workflow used by the app.
"""
        )

        workflow_steps = [
            "1. Accept user role, purpose, task type, and public source text.",
            "2. Validate whether enough public source text was provided.",
            "3. Send the request to an LLM router tool called select_trendlens_route.",
            "4. Use the LLM route to dispatch generation to the selected model.",
            "5. Send the selected model a real function schema called analyze_public_sources.",
            "6. Let the generation model request the function tool.",
            "7. Execute the Python function only after the model requests it.",
            "8. Return the tool result to the model.",
            "9. Generate the final situational awareness report from the tool result.",
            "10. Save the report, feedback, and evaluation record as app actions.",
        ]

        for step in workflow_steps:
            st.write(step)

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric("Valid sources detected", valid_source_count)

        with col_b:
            st.metric("Selected sections", len(selected_sections))

        with col_c:
            if st.session_state.get("latest_routing_decision"):
                st.metric(
                    "Last LLM route",
                    st.session_state.latest_routing_decision.get(
                        "route_display_name", "Route selected"
                    ),
                )
            else:
                st.metric("LLM route", "Selected after Generate")

        st.caption(
            "P3 update: the app no longer only changes prompt text. When Generate is clicked, an LLM router chooses the route, and the app dispatches to the model assigned to that route."
        )

def render_source_input(source_number, required=False):
    required_text = "Required" if required else "Optional"

    with st.expander(f"Source {source_number} | {required_text}", expanded=required):
        source_type = st.selectbox(
            f"Source {source_number} type",
            [
                "Article",
                "Public safety alert",
                "Government update",
                "Weather statement",
                "Incident report",
                "Social media post",
                "Public event summary",
                "Other",
            ],
            key=f"source_{source_number}_type",
        )

        source_label = st.text_input(
            f"Source {source_number} label",
            value=f"Source {source_number}",
            key=f"source_{source_number}_label",
            help="Example: Local news article, city alert, public safety update",
        )

        source_url = st.text_input(
            f"Source {source_number} URL",
            value="",
            key=f"source_{source_number}_url",
            help="Optional public URL or source link",
        )

        source_text = st.text_area(
            f"Paste Source {source_number} text",
            height=220,
            key=f"source_{source_number}_text",
            placeholder="Paste public or synthetic source text here.",
        )

    return {
        "type": source_type,
        "label": source_label,
        "url": source_url,
        "text": source_text,
    }


def render_report_section_selector():
    st.subheader("Select Desired Report Sections")

    section_options = [
        "Source Overview",
        "Raw Tracker Entry",
        "Bottom Line Up Front",
        "Executive Summary",
        "Key Facts",
        "Timeline",
        "So What / Why This Matters",
        "Source Comparison and Reliability Notes",
        "Confidence Assessment",
        "Trend and Pattern Analysis",
        "Trend and Anomaly Detection",
        "Second and Third Order Effects",
        "Follow Up Questions / RFIs",
        "Forty Five Second Brief",
    ]

    selected_sections = st.multiselect(
        "Choose the sections to include in the generated report.",
        options=section_options,
        default=st.session_state.selected_sections,
    )

    st.session_state.selected_sections = selected_sections

    return selected_sections



def render_generate_report_tab():
    st.header("1. Define User Role and Report Purpose")

    with st.expander("Help / Quick Start", expanded=False):
        st.markdown(
            """
    - Step 1: Choose audience and report purpose.
    - Step 2: Paste public or synthetic sources.
    - Step 3: Select report sections.
    - Step 4: Generate report.
    - Step 5: Review the LLM routing decision, selected model, confidence, source comparison, gaps, RFIs, and 45-second brief.

    **Safety note:** Do not enter classified, private, sensitive, protected, or restricted data.
    """
        )

    left_column, right_column = st.columns(2)

    with left_column:
        target_audience = st.selectbox(
            "Who is the report for?",
            [
                "Intelligence Analyst",
                "Emergency Responder",
                "Public Audience",
                "Emergency Management Personnel",
                "Researcher / Student",
                "Journalist",
                "Security Professional",
                "Organization Leader",
            ],
        )

        task_type = st.selectbox(
            "What type of task should the system perform?",
            [
                "Generate situational awareness report",
                "Compare public sources",
                "Create executive briefing",
                "Create raw tracker entry",
                "Identify trends and anomalies",
                "Generate follow up questions and RFIs",
                "Monitoring update",
            ],
        )

    with right_column:
        output_depth = st.selectbox(
            "How detailed should the report be?",
            [
                "Concise",
                "Standard",
                "Detailed",
            ],
            index=1,
        )

        report_purpose = st.text_area(
            "What is the purpose of this report?",
            height=120,
            placeholder=(
                "Example: Compare public reporting on a developing event and create a short situational awareness update."
            ),
        )

    st.divider()

    st.header("2. Add Public Information Sources")

    st.info(
        "Use only public or synthetic information. Do not paste classified, private, restricted, or sensitive information."
    )

    source_1 = render_source_input(1, required=True)
    source_2 = render_source_input(2, required=False)
    source_3 = render_source_input(3, required=False)

    sources = build_source_payload(source_1, source_2, source_3)
    valid_source_count = len(sources)

    source_errors, source_warnings = validate_public_sources(sources)

    for warning in source_warnings:
        st.warning(warning)

    for error in source_errors:
        st.error(error)

    st.write(f"Valid sources detected: {valid_source_count}")

    st.divider()

    st.header("3. Choose Report Outputs")

    selected_sections = render_report_section_selector()

    custom_instructions = st.text_area(
        "Optional custom instructions",
        height=120,
        placeholder=(
            "Example: Keep the report concise, use active voice, include second and third order effects, and avoid unsupported assumptions."
        ),
    )

    st.divider()

    st.header("4. Agentic Workflow and LLM Model Routing")

    if st.session_state.get("show_workflow_preview", True):
        render_agent_workflow_panel(valid_source_count, selected_sections)

    with st.expander("Available model routes", expanded=False):
        route_catalog = get_route_catalog()

        st.write(
            "The LLM router chooses one of these routes after you click Generate. The app then uses the model assigned to that route."
        )

        for route_name, route_data in route_catalog.items():
            st.markdown(
                f"**{route_data['display_name']}**  \n"
                f"Route key: `{route_name}`  \n"
                f"Model: `{route_data['selected_model']}`  \n"
                f"Configured by: `{route_data['model_key']}`  \n"
                f"{route_data['route_instructions']}"
            )

    st.divider()

    st.header("5. Generate Report")

    if not OPENAI_AVAILABLE:
        st.error(
            "The openai package is not installed. Install it with: pip install openai"
        )

    if not get_openai_api_key():
        st.warning(
            "OPENAI_API_KEY is not set. The report will not generate until the key is added to Streamlit secrets or the local environment."
        )

    generate_button = st.button(
        "Generate TrendLens Report",
        type="primary",
        use_container_width=True,
    )

    if generate_button:
        if source_errors:
            st.error("Fix the source input issues before generating a report.")
            st.stop()
        elif valid_source_count == 0:
            st.error("Paste at least one public source before generating a report.")
        elif not report_purpose.strip():
            st.error("Enter a report purpose before generating a report.")
        elif not selected_sections:
            st.error("Select at least one report section before generating a report.")
        else:
            with st.spinner("Selecting LLM route, dispatching model, and generating report..."):
                try:
                    routing_decision = route_model_behavior_with_llm(
                        sources=sources,
                        target_audience=target_audience,
                        report_purpose=report_purpose,
                        selected_sections=selected_sections,
                        task_type=task_type,
                        output_depth=output_depth,
                    )

                    metadata = build_metadata(
                        target_audience=target_audience,
                        report_purpose=report_purpose,
                        task_type=task_type,
                        output_depth=output_depth,
                        selected_sections=selected_sections,
                        sources=sources,
                        routing_decision=routing_decision,
                    )

                    report, tool_trace = run_model_tool_workflow(
                        sources=sources,
                        target_audience=target_audience,
                        report_purpose=report_purpose,
                        selected_sections=selected_sections,
                        custom_instructions=custom_instructions,
                        task_type=task_type,
                        output_depth=output_depth,
                        routing_decision=routing_decision,
                    )

                    metadata["generation_mode"] = "llm routed model callable tool workflow"
                    metadata["model_tool_used"] = "analyze_public_sources"
                    metadata["tool_requested_by_model"] = tool_trace.get(
                        "tool_requested_by_model", False
                    )

                    st.session_state.latest_report = report
                    st.session_state.latest_metadata = metadata
                    st.session_state.latest_tool_trace = tool_trace
                    st.session_state.latest_routing_decision = routing_decision
                    st.session_state.latest_generation_mode = (
                        "llm routed model callable tool workflow"
                    )
                    st.session_state.feedback_saved = False
                    st.session_state.eval_saved = False

                    st.success(
                        "Report generated with LLM model routing and real model callable tool use."
                    )

                except Exception as error:
                    st.error("The report could not be generated.")
                    st.exception(error)

    if st.session_state.latest_report:
        st.divider()
        st.header("Generated Report")

        if st.session_state.latest_generation_mode:
            st.caption(f"Generation mode: {st.session_state.latest_generation_mode}")

        if st.session_state.latest_routing_decision:
            with st.expander("LLM routing decision", expanded=True):
                route = st.session_state.latest_routing_decision

                col_route, col_model, col_confidence = st.columns(3)

                with col_route:
                    st.metric(
                        "Route selected",
                        route.get("route_display_name", route.get("route_name", "")),
                    )

                with col_model:
                    st.metric("Generation model", route.get("selected_model", ""))

                with col_confidence:
                    st.metric("Route confidence", route.get("confidence", ""))

                st.write(f"Reason: {route.get('reason', '')}")

                if route.get("evidence_from_input"):
                    st.write("Evidence from input:")
                    for item in route.get("evidence_from_input", []):
                        st.write(f"• {item}")

                with st.expander("Full routing JSON", expanded=False):
                    st.json(route)

        if st.session_state.latest_tool_trace:
            with st.expander("Model tool use trace", expanded=True):
                st.json(st.session_state.latest_tool_trace)

        st.markdown(st.session_state.latest_report)

        col_save, col_download = st.columns(2)

        with col_save:
            if st.button("Save Report", use_container_width=True):
                try:
                    saved_path = call_save_report(
                        st.session_state.latest_report,
                        st.session_state.latest_metadata,
                    )

                    st.session_state.latest_report_path = str(saved_path)

                    st.success("Report saved.")
                    st.write(f"Saved to: {saved_path}")

                except Exception as error:
                    st.error("The report could not be saved.")
                    st.exception(error)

        with col_download:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                "Download Report as Markdown",
                data=st.session_state.latest_report,
                file_name=f"trendlens_report_{timestamp}.md",
                mime="text/markdown",
                use_container_width=True,
            )

        st.divider()

        st.header("Evaluation Record")

        st.markdown(
            """
Use this section to satisfy the expected versus actual output requirement. After generating one report, enter the expected behavior and save the actual report output as the evaluation record.
"""
        )

        default_expected_output = (
            "The app should use an LLM tool call named select_trendlens_route to choose the best route, "
            "dispatch generation to the selected model, call analyze_public_sources before writing the final report, "
            "include the selected report sections, compare the pasted public sources, identify information gaps, "
            "include a confidence assessment, and avoid unsupported claims."
        )

        expected_output = st.text_area(
            "Expected output",
            value=default_expected_output,
            height=140,
            key="expected_eval_output",
        )

        actual_output = st.text_area(
            "Actual output",
            value=st.session_state.latest_report,
            height=220,
            key="actual_eval_output",
        )

        if st.button("Save Evaluation Record", use_container_width=True):
            if not expected_output.strip() or not actual_output.strip():
                st.error("Expected output and actual output are required.")
            else:
                try:
                    eval_path = save_eval_record(
                        expected_output=expected_output,
                        actual_output=actual_output,
                        metadata=st.session_state.latest_metadata,
                        tool_trace=st.session_state.latest_tool_trace,
                    )

                    st.session_state.eval_saved = True

                    st.success("Evaluation record saved.")
                    st.write(f"Saved to: {eval_path}")

                except Exception as error:
                    st.error("The evaluation record could not be saved.")
                    st.exception(error)

        st.divider()

        st.header("Feedback")

        feedback_rating = st.slider(
            "How useful was this report?",
            min_value=1,
            max_value=5,
            value=4,
        )

        feedback_text = st.text_area(
            "What should be improved?",
            height=120,
            placeholder="Example: The report was useful, but it needs clearer confidence language.",
        )

        if st.button("Save Feedback"):
            if not feedback_text.strip():
                st.error("Enter feedback before saving.")
            else:
                feedback_metadata = dict(st.session_state.latest_metadata)
                feedback_metadata["latest_report_path"] = st.session_state.latest_report_path

                try:
                    feedback_path = call_save_feedback(
                        feedback_text=feedback_text,
                        rating=feedback_rating,
                        metadata=feedback_metadata,
                    )

                    st.session_state.feedback_saved = True

                    st.success("Feedback saved.")
                    st.write(f"Saved to: {feedback_path}")

                except Exception as error:
                    st.error("Feedback could not be saved.")
                    st.exception(error)

def render_monitoring_tab():
    st.header("Semi Automated Monitoring")

    st.markdown(
        """
This section supports the planned monitoring workflow for Project 2. The goal is to let a user track a public topic and check for updates on a user selected interval.
"""
    )

    st.info(
        "For the working draft, monitoring is semi automated. The user still controls the topic, reviews changes, and validates the final report."
    )

    if not MONITORING_AVAILABLE:
        st.warning(
            "Monitoring tools are not loaded yet. Confirm monitoring.py exists in the project folder."
        )

        if MONITORING_IMPORT_ERROR:
            st.caption(f"Current monitoring import message: {MONITORING_IMPORT_ERROR}")

        return

    with st.form("monitoring_topic_form"):
        topic_name = st.text_input(
            "Monitoring topic or event",
            placeholder="Example: chemical spill in a specific city, severe weather event, public safety incident",
        )

        topic_description = st.text_area(
            "Monitoring purpose",
            placeholder="Describe what updates should matter for this topic.",
            height=120,
        )

        source_url = st.text_input(
            "Primary public source URL",
            placeholder="Optional public website or source link",
        )

        check_frequency_label = st.selectbox(
            "How often should the agent check for updates?",
            [
                "5 minutes",
                "15 minutes",
                "30 minutes",
                "1 hour",
                "2 hours",
                "4 hours",
                "5 hours",
                "12 hours",
                "24 hours",
            ],
            index=6,
        )

        check_frequency_map = {
            "5 minutes": 5,
            "15 minutes": 15,
            "30 minutes": 30,
            "1 hour": 60,
            "2 hours": 120,
            "4 hours": 240,
            "5 hours": 300,
            "12 hours": 720,
            "24 hours": 1440,
        }

        check_interval_minutes = check_frequency_map[check_frequency_label]

        submit_monitoring_topic = st.form_submit_button("Save Monitoring Topic")

    if submit_monitoring_topic:
        if not topic_name.strip():
            st.error("Enter a monitoring topic before saving.")
        else:
            topic_data = {
                "topic_name": topic_name.strip(),
                "topic_description": topic_description.strip(),
                "source_url": source_url.strip(),
                "check_interval_minutes": check_interval_minutes,
                "check_frequency_label": check_frequency_label,
                "check_interval_hours": max(1, round(check_interval_minutes / 60)),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            saved_path = save_monitored_topic(topic_data)
            st.success("Monitoring topic saved.")
            st.write(f"Saved to: {saved_path}")

    st.divider()

    st.subheader("Manual Change Detection Test")

    st.markdown(
        """
Use this test to prove the monitoring logic can compare older source text against updated source text.
"""
    )

    previous_text = st.text_area(
        "Previous source text",
        height=180,
        key="previous_monitoring_text",
        placeholder="Paste the older or baseline version of the source text here.",
    )

    updated_text = st.text_area(
        "Updated source text",
        height=180,
        key="updated_monitoring_text",
        placeholder="Paste the newer version of the source text here.",
    )

    if st.button("Compare Source Text"):
        if not previous_text.strip() or not updated_text.strip():
            st.error("Paste both previous text and updated text before comparing.")
        else:
            change_result = compare_source_changes(previous_text, updated_text)

            st.subheader("Change Detection Result")

            if isinstance(change_result, dict):
                summary_col_1, summary_col_2, summary_col_3 = st.columns(3)

                with summary_col_1:
                    st.metric("Changed", str(change_result.get("changed", False)))

                with summary_col_2:
                    st.metric(
                        "Meaningful Change",
                        str(change_result.get("meaningful_change", False)),
                    )

                with summary_col_3:
                    st.metric(
                        "Similarity Score",
                        change_result.get("similarity_score", "N/A"),
                    )

                st.write(change_result.get("change_summary", ""))

                line_changes = change_result.get("line_changes", {})

                with st.expander("Added lines"):
                    added_lines = line_changes.get("added_lines", [])

                    if added_lines:
                        for line in added_lines:
                            st.write(f"• {line}")
                    else:
                        st.write("No added lines detected.")

                with st.expander("Removed lines"):
                    removed_lines = line_changes.get("removed_lines", [])

                    if removed_lines:
                        for line in removed_lines:
                            st.write(f"• {line}")
                    else:
                        st.write("No removed lines detected.")

                with st.expander("Full JSON result"):
                    st.json(change_result)
            else:
                st.write(change_result)

    st.divider()

    st.subheader("Saved Monitoring Topics")

    try:
        topics = load_monitored_topics()

        if not topics:
            st.write("No monitoring topics saved yet.")
        else:
            st.json(topics)

    except Exception as error:
        st.error(f"Could not load monitoring topics: {error}")


def render_report_library_tab():
    st.header("Report Library")

    st.info(
        "Coming soon: this tab will show saved reports, searchable report history, and downloadable outputs."
    )

    st.subheader("Planned Features")

    st.markdown(
        """
1. Saved report history.
2. Searchable prior reports.
3. Download previous reports.
4. Filter reports by audience, task type, date, or confidence level.
5. Compare current reports against earlier reports.
"""
    )

    st.subheader("Current Working Draft Note")

    st.write(
        "Reports can currently be saved from the Generate Report tab and downloaded as Markdown files."
    )


def render_alert_center_tab():
    st.header("Alert Center")

    st.info(
        "Coming soon: this tab will show meaningful change alerts, monitoring topic status, and future notification settings."
    )

    st.subheader("Planned Features")

    st.markdown(
        """
1. Meaningful change alerts.
2. Monitoring topic status.
3. Last checked timestamps.
4. Email alert settings.
5. Notification history.
6. Human review queue for updated reports.
"""
    )

    st.subheader("Current Working Draft Note")

    st.write(
        "The current app supports manual old versus new source comparison in the Monitoring Workflow tab. Full email alerts would require persistent storage and an external background worker."
    )


def render_analytics_tab():
    st.header("Analytics")

    st.info(
        "Coming soon: this tab will visualize reporting trends, source patterns, and monitoring activity."
    )

    st.subheader("Planned Features")

    st.markdown(
        """
1. Source type breakdown.
2. Report generation totals.
3. Confidence level trends.
4. Monitoring activity trends.
5. Event category summaries.
6. Common Request for Information themes.
"""
    )

    st.subheader("Current Working Draft Note")

    st.write(
        "This placeholder shows the future analytics direction while keeping the current draft focused on source intake, report generation, feedback, monitoring, and evaluation."
    )



def render_about_tab():
    st.header("About TrendLens AI")

    st.markdown(
        """
TrendLens AI is a classroom Project 2 / Project 3 working draft focused on agentic AI systems.

The application is designed to demonstrate:

1. Reasoning based event categorization.
2. Structured reporting workflows.
3. Trend and pattern analysis.
4. Contextual memory through saved outputs.
5. Adaptive output generation.
6. Analyst style briefing products.
7. Real model callable tool use.
8. Feedback logging.
9. Semi automated monitoring.
10. LLM tool based model routing.
11. Model Context Protocol style architecture.
12. Expected versus actual evaluation logging.

The primary audience is the intelligence analyst. Secondary audiences include emergency responders and the public.
"""
    )

    st.subheader("How the Agentic Workflow Works")

    st.graphviz_chart(
        """
        digraph {
            rankdir=LR;

            user_input [label="User enters public sources"];
            validation [label="Source intake and validation"];
            router_model [label="Router model"];
            route_tool [label="select_trendlens_route tool call"];
            model_dispatch [label="Dispatch to selected model"];
            tool_schema [label="Function schema sent to selected model"];
            model_tool_call [label="Model requests analyze_public_sources"];
            app_tool [label="App executes Python analysis tool"];
            tool_result [label="Tool result returned to model"];
            report_output [label="Structured report"];
            eval_record [label="Expected vs actual eval record"];
            save_report [label="Save report"];
            feedback [label="Save feedback"];
            monitoring [label="Monitoring workflow"];
            change_detection [label="Old vs new source comparison"];
            updated_report [label="Updated report for review"];

            user_input -> validation;
            validation -> router_model;
            router_model -> route_tool;
            route_tool -> model_dispatch;
            model_dispatch -> tool_schema;
            tool_schema -> model_tool_call;
            model_tool_call -> app_tool;
            app_tool -> tool_result;
            tool_result -> report_output;
            report_output -> eval_record;
            report_output -> save_report;
            report_output -> feedback;
            validation -> monitoring;
            monitoring -> change_detection;
            change_detection -> updated_report;
        }
        """
    )

    st.subheader("P3 Routing Explanation")

    st.write(
        "This version uses LLM tool based routing. When the user clicks Generate, the router model must call select_trendlens_route. The app reads that route decision, maps it to a configured generation model, and dispatches report generation to that selected model. The selected model must then call analyze_public_sources before writing the final report."
    )

    st.subheader("Current Model Route Configuration")

    for route_name, route_data in get_route_catalog().items():
        st.markdown(
            f"**{route_data['display_name']}**  \n"
            f"Route key: `{route_name}`  \n"
            f"Model: `{route_data['selected_model']}`  \n"
            f"Environment key: `{route_data['model_key']}`"
        )

    st.subheader("Deployment Check")

    st.write(
        "If this page loaded, the deployed Streamlit app is awake at runtime. Record this run in BUILD_LOG.md after testing the deployed link."
    )

    st.write(f"App loaded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    st.subheader("Data Safety Notice")

    st.warning(
        """
Only use public or synthetic information. Do not enter classified, private, restricted, protected, or sensitive information.
"""
    )

def render_security_tab():
    st.header("Security / Login")

    st.markdown(
        """
Demo mode is open by default so an instructor can grade the app without requiring login.

To require authentication in production, set the environment variable `TRENDLENS_AUTH_REQUIRED=true` or add it to Streamlit secrets.

This app is designed to integrate with Streamlit OIDC authentication providers such as Google, Microsoft, Okta, or Auth0. MFA is handled by the identity provider.

The app does not store passwords or MFA codes. Store secrets like OIDC client IDs and client secrets in `.streamlit/secrets.toml` locally or use Streamlit Cloud secrets — do not commit them to GitHub.

The source intake fields are validated for possible sensitive markers before generation. Use the Generate Report tab to see validation warnings or errors.
"""
    )

    # Also render the sidebar auth gate to give users consistent controls
    try:
        render_auth_gate()
    except Exception:
        st.info("Authentication controls are available in the sidebar when configured.")


initialize_session_state()
ensure_project_folders()
render_header()
if st.session_state.get("show_welcome_video", True):
    render_welcome_video()


main_tab, monitoring_tab, report_library_tab, alert_center_tab, analytics_tab, security_tab, about_tab = st.tabs(
    [
        "Generate Report",
        "Monitoring Workflow",
        "Report Library",
        "Alert Center",
        "Analytics",
        "Security / Login",
        "About",
    ]
)


with main_tab:
    render_generate_report_tab()


with monitoring_tab:
    render_monitoring_tab()


with report_library_tab:
    render_report_library_tab()


with alert_center_tab:
    render_alert_center_tab()


with analytics_tab:
    render_analytics_tab()


with security_tab:
    render_security_tab()

with about_tab:
    render_about_tab()
