import json
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image, UnidentifiedImageError

from trend_tools import generate_trendlens_report, save_feedback, save_report


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

ICON_PATH = ASSETS_DIR / "trendlens-icon.png"
BANNER_PATH = ASSETS_DIR / "trendlens-banner.png"


def safe_load_image(image_path):
    """
    Safely loads an image file.

    This prevents the Streamlit app from crashing if an image exists but is empty,
    corrupted, or not a real PNG file.
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


def initialize_session_state():
    if "latest_report" not in st.session_state:
        st.session_state.latest_report = ""

    if "latest_report_path" not in st.session_state:
        st.session_state.latest_report_path = ""

    if "latest_metadata" not in st.session_state:
        st.session_state.latest_metadata = {}

    if "feedback_saved" not in st.session_state:
        st.session_state.feedback_saved = False

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


def ensure_project_folders():
    OUTPUTS_DIR.mkdir(exist_ok=True)
    MONITORING_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)


def route_model_behavior(target_audience, task_type):
    audience = target_audience.lower()
    task = task_type.lower()

    if "monitor" in task or "update" in task:
        return "Monitoring Update Route"

    if "intelligence" in audience:
        return "Intelligence Analyst Route"

    if "emergency" in audience:
        return "Emergency Responder Route"

    if "public" in audience:
        return "Public Audience Route"

    if "journalist" in audience:
        return "Journalist / Research Route"

    if "security" in audience:
        return "Security Professional Route"

    return "General Situational Awareness Route"


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
    model_route,
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
        "model_route": model_route,
    }


def call_report_generator(
    sources,
    target_audience,
    report_purpose,
    selected_sections,
    custom_instructions,
    task_type,
    output_depth,
    model_route,
):
    try:
        return generate_trendlens_report(
            sources=sources,
            target_audience=target_audience,
            report_purpose=report_purpose,
            selected_sections=selected_sections,
            custom_instructions=custom_instructions,
            task_type=task_type,
            output_depth=output_depth,
            model_route=model_route,
        )
    except TypeError:
        pass

    try:
        return generate_trendlens_report(
            target_audience,
            report_purpose,
            selected_sections,
            custom_instructions,
            sources,
        )
    except TypeError:
        pass

    combined_sources = ""

    for source in sources:
        combined_sources += f"""
Source {source.get("source_number")}
Type: {source.get("type")}
Label: {source.get("label")}
URL: {source.get("url")}

Text:
{source.get("text")}

"""

    return generate_trendlens_report(
        combined_sources,
        target_audience,
        report_purpose,
        selected_sections,
        custom_instructions,
    )


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


def render_header():
    if banner_image is not None:
        st.image(banner_image, use_container_width=True)
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

For this working draft, paste two or three public article excerpts, alerts, reports, updates, or event descriptions. The system compares the sources and generates an analyst style report with source overview, Bottom Line Up Front, executive summary, confidence assessment, source comparison, and follow up questions.
"""
    )


def render_agent_workflow_panel(valid_source_count, selected_sections, model_route):
    with st.expander("Agent workflow preview", expanded=True):
        st.markdown(
            """
This panel shows how the application behaves like an agentic workflow instead of a basic chat box.
"""
        )

        workflow_steps = [
            "1. Accept user role, purpose, task type, and public source text.",
            "2. Validate whether enough public source text was provided.",
            "3. Route the task to the correct model behavior.",
            "4. Generate a structured situational awareness report.",
            "5. Save the report output as an action.",
            "6. Save user feedback as an evaluation action.",
            "7. Support future monitoring checks for updated public information.",
        ]

        for step in workflow_steps:
            st.write(step)

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric("Valid sources detected", valid_source_count)

        with col_b:
            st.metric("Selected sections", len(selected_sections))

        with col_c:
            st.metric("Model route", model_route)


def render_source_input(source_number, required=False):
    required_text = "Required" if required else "Optional"

    with st.expander(f"Source {source_number} - {required_text}", expanded=required):
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

    model_route = route_model_behavior(target_audience, task_type)

    st.divider()

    st.header("4. Agentic Workflow and Model Routing")

    render_agent_workflow_panel(valid_source_count, selected_sections, model_route)

    st.divider()

    st.header("5. Generate Report")

    generate_button = st.button(
        "Generate TrendLens Report",
        type="primary",
        use_container_width=True,
    )

    if generate_button:
        if valid_source_count == 0:
            st.error("Paste at least one public source before generating a report.")
        elif not report_purpose.strip():
            st.error("Enter a report purpose before generating a report.")
        elif not selected_sections:
            st.error("Select at least one report section before generating a report.")
        else:
            metadata = build_metadata(
                target_audience=target_audience,
                report_purpose=report_purpose,
                task_type=task_type,
                output_depth=output_depth,
                selected_sections=selected_sections,
                sources=sources,
                model_route=model_route,
            )

            with st.spinner("Generating structured situational awareness report..."):
                try:
                    report = call_report_generator(
                        sources=sources,
                        target_audience=target_audience,
                        report_purpose=report_purpose,
                        selected_sections=selected_sections,
                        custom_instructions=custom_instructions,
                        task_type=task_type,
                        output_depth=output_depth,
                        model_route=model_route,
                    )

                    st.session_state.latest_report = report
                    st.session_state.latest_metadata = metadata
                    st.session_state.feedback_saved = False

                    st.success("Report generated.")

                except Exception as error:
                    st.error("The report could not be generated.")
                    st.exception(error)

    if st.session_state.latest_report:
        st.divider()
        st.header("Generated Report")

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
        "This placeholder shows the future analytics direction while keeping the current draft focused on source intake, report generation, feedback, and monitoring."
    )


def render_about_tab():
    st.header("About TrendLens AI")

    st.markdown(
        """
TrendLens AI is a classroom Project 2 working draft focused on agentic AI systems.

The application is designed to demonstrate:

1. Reasoning based event categorization.
2. Structured reporting workflows.
3. Trend and pattern analysis.
4. Contextual memory.
5. Adaptive output generation.
6. Analyst style briefing products.
7. Tool based actions.
8. Feedback logging.
9. Semi automated monitoring.
10. Model routing.
11. Model Context Protocol style architecture.

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
            routing [label="Model routing"];
            report_tool [label="Report generation tool"];
            report_output [label="Structured report"];
            save_report [label="Save report"];
            feedback [label="Save feedback"];
            monitoring [label="Monitoring workflow"];
            change_detection [label="Old vs new source comparison"];
            updated_report [label="Updated report for review"];

            user_input -> validation;
            validation -> routing;
            routing -> report_tool;
            report_tool -> report_output;
            report_output -> save_report;
            report_output -> feedback;
            validation -> monitoring;
            monitoring -> change_detection;
            change_detection -> updated_report;
        }
        """
    )

    st.subheader("Data Safety Notice")

    st.warning(
        """
Only use public or synthetic information. Do not enter classified, private, restricted, protected, or sensitive information.
"""
    )


initialize_session_state()
ensure_project_folders()
render_header()


main_tab, monitoring_tab, report_library_tab, alert_center_tab, analytics_tab, about_tab = st.tabs(
    [
        "Generate Report",
        "Monitoring Workflow",
        "Report Library",
        "Alert Center",
        "Analytics",
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


with about_tab:
    render_about_tab()