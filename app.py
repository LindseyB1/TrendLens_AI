import streamlit as st

from trend_tools import (
    generate_trendlens_report,
    get_agent_workflow_summary,
    save_feedback,
    save_report,
)


st.set_page_config(
    page_title="TrendLens AI",
    page_icon="📊",
    layout="wide",
)


if "latest_report" not in st.session_state:
    st.session_state.latest_report = ""

if "latest_report_path" not in st.session_state:
    st.session_state.latest_report_path = ""

if "latest_agent_workflow" not in st.session_state:
    st.session_state.latest_agent_workflow = ""


def source_input(source_number: int, label_placeholder: str, required: bool = False) -> dict:
    st.subheader(f"Source {source_number}")

    st.caption("Required source" if required else "Optional source")

    source_type = st.selectbox(
        f"Source {source_number} type",
        [
            "Article",
            "Government source",
            "Press release",
            "Public alert",
            "Social media post",
            "Report",
            "Field note",
            "Other public source",
        ],
        key=f"source_{source_number}_type",
    )

    source_label = st.text_input(
        f"Source {source_number} label",
        placeholder=label_placeholder,
        key=f"source_{source_number}_label",
    )

    source_url = st.text_input(
        f"Source {source_number} URL",
        placeholder="Optional URL or source link",
        key=f"source_{source_number}_url",
    )

    source_text = st.text_area(
        f"Paste Source {source_number} text",
        height=180,
        key=f"source_{source_number}_text",
    )

    return {
        "type": source_type,
        "label": source_label,
        "url": source_url,
        "text": source_text,
    }


st.title("TrendLens AI")
st.caption("Multi source public event analysis and situational awareness reporting assistant")

st.markdown(
    """
TrendLens AI helps users turn varied public information sources into one structured situational awareness product.

For this project draft, users can paste public articles, alerts, reports, updates, or event descriptions. The system compares the sources, identifies key patterns, and generates a customized intelligence style report based on the user role and selected output sections.
"""
)

st.info(
    "Use only public or synthetic information. Do not paste classified, private, sensitive, or restricted information."
)

with st.sidebar:
    st.header("TrendLens Draft Scope")

    st.markdown(
        """
This draft focuses on multi source ingestion, source comparison, and structured intelligence reporting.

The current version uses one main TrendLens Analysis Agent with a step based workflow:
Source Intake, Source Normalization, Source Comparison, Trend Extraction, Risk Assessment, Confidence Assessment, and Report Generation.
"""
    )

    st.divider()

    if st.session_state.latest_report:
        st.success("A report has been generated in this session.")
    else:
        st.warning("No report generated yet.")


st.divider()

st.header("1. Define User Role and Report Purpose")

user_role = st.selectbox(
    "Who is the report for?",
    [
        "Intelligence Analyst",
        "Emergency Manager",
        "Student",
        "Business Leader",
        "General Public",
        "Other",
    ],
)

report_purpose = st.text_area(
    "What is the purpose of this report?",
    placeholder="Example: Prepare a commander update, summarize a developing public event, compare conflicting sources, or identify second and third order effects.",
    height=120,
)

with st.expander("Need ideas for the report purpose?"):
    st.markdown(
        """
Examples:
        
Prepare a short situational awareness update.

Compare public reporting on a developing event.

Identify what changed and why it matters.

Create a commander style update.

Summarize public safety concerns.

Identify second and third order effects.

Turn multiple public sources into one briefable intelligence product.
"""
    )

st.divider()

st.header("2. Add Public Information Sources")

st.caption(
    "For this draft, paste up to three sources. Future versions can expand to additional uploads or larger source batches."
)

source_1 = source_input(
    source_number=1,
    label_placeholder="Example: Local news article, city alert, public safety update",
    required=True,
)

source_2 = source_input(
    source_number=2,
    label_placeholder="Example: National article, official statement, press release",
)

source_3 = source_input(
    source_number=3,
    label_placeholder="Example: Optional third source, related update, background source",
)

sources = [source_1, source_2, source_3]
valid_sources = [source for source in sources if source["text"].strip() or source["url"].strip()]

st.divider()

st.header("3. Select Desired Report Sections")

st.caption("Select the sections the user wants included in the final output.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    include_source_overview = st.checkbox("Source Overview", value=True)
    include_bluf = st.checkbox("BLUF", value=True)
    include_exec_summary = st.checkbox("Executive Summary", value=True)
    include_5ws = st.checkbox("5 Ws", value=True)
    include_so_what = st.checkbox("So What or Why This Matters", value=True)

with col2:
    include_key_judgments = st.checkbox("Key Judgments", value=True)
    include_key_trends = st.checkbox("Key Trends", value=True)
    include_conditions = st.checkbox("Conditions, Circumstances, and Influences", value=True)
    include_source_comparison = st.checkbox("Source Comparison and Reliability Notes", value=True)
    include_risks = st.checkbox("Risks and Concerns", value=True)

with col3:
    include_safety = st.checkbox("Safety Considerations", value=False)
    include_second_order = st.checkbox("Second Order Effects", value=True)
    include_third_order = st.checkbox("Third Order Effects", value=True)
    include_indicators = st.checkbox("Indicators", value=True)
    include_assessment = st.checkbox("Assessment", value=True)

with col4:
    include_collection_gaps = st.checkbox("Collection Gaps", value=True)
    include_confidence = st.checkbox("Confidence Assessment", value=True)
    include_follow_up = st.checkbox("Recommended Follow Up Questions", value=True)
    include_45_second_brief = st.checkbox("45 Second Brief", value=True)
    include_graphical_summary = st.checkbox("Graphical Summary Table", value=False)

with st.expander("What can the output include?"):
    st.markdown(
        """
TrendLens can produce a short BLUF, executive summary, 5 Ws, source overview, source comparison, key judgments, risks, second and third order effects, indicators, collection gaps, confidence assessment, recommended follow up questions, and a 45 second brief.

The Graphical Summary Table option creates a markdown table. It does not create actual images, maps, or charts in this draft.
"""
    )

custom_output_request = st.text_area(
    "Optional custom output request",
    placeholder="Example: Tailor this for a battalion commander, include aviation impacts, or focus on public safety concerns.",
    height=100,
)

selected_outputs = {
    "Source Overview": include_source_overview,
    "BLUF": include_bluf,
    "Executive Summary": include_exec_summary,
    "5 Ws": include_5ws,
    "So What or Why This Matters": include_so_what,
    "Key Judgments": include_key_judgments,
    "Key Trends": include_key_trends,
    "Conditions, Circumstances, and Influences": include_conditions,
    "Source Comparison and Reliability Notes": include_source_comparison,
    "Risks and Concerns": include_risks,
    "Safety Considerations": include_safety,
    "Second Order Effects": include_second_order,
    "Third Order Effects": include_third_order,
    "Indicators": include_indicators,
    "Assessment": include_assessment,
    "Collection Gaps": include_collection_gaps,
    "Confidence Assessment": include_confidence,
    "Recommended Follow Up Questions": include_follow_up,
    "45 Second Brief": include_45_second_brief,
    "Graphical Summary Table": include_graphical_summary,
}

st.divider()

st.header("4. Generate TrendLens Report")

st.write(
    "The report will compare the submitted public sources and generate one structured situational awareness product."
)

st.caption(f"Valid sources detected: {len(valid_sources)}")

generate_button = st.button("Generate TrendLens Report", type="primary")

if generate_button:
    if len(valid_sources) < 1:
        st.warning("Please paste at least one public information source or URL before generating a report.")
    else:
        with st.spinner("Analyzing sources and generating structured report..."):
            report = generate_trendlens_report(
                valid_sources,
                user_role=user_role,
                report_purpose=report_purpose,
                selected_outputs=selected_outputs,
                custom_output_request=custom_output_request,
            )

            st.session_state.latest_report = report
            st.session_state.latest_agent_workflow = get_agent_workflow_summary(valid_sources)

            if report.startswith("Error"):
                st.session_state.latest_report_path = ""
                st.error(report)
            else:
                report_path = save_report(report)
                st.session_state.latest_report_path = report_path


if st.session_state.latest_report:
    st.divider()
    st.header("5. TrendLens AI Report")

    if st.session_state.latest_report.startswith("Error"):
        st.error(st.session_state.latest_report)
    else:
        st.markdown(st.session_state.latest_report)

        if st.session_state.latest_report_path:
            st.success(f"Report saved locally to: {st.session_state.latest_report_path}")

        st.download_button(
            label="Download Report as Markdown",
            data=st.session_state.latest_report,
            file_name="trendlens_report.md",
            mime="text/markdown",
        )

        st.divider()
        st.header("6. Agent Workflow Used")

        st.markdown(st.session_state.latest_agent_workflow)

        st.divider()
        st.header("7. Feedback")

        feedback_choice = st.selectbox(
            "How useful was this report?",
            [
                "Select feedback",
                "Useful and specific",
                "Too broad",
                "Missing important context",
                "Needs clearer trends",
                "Needs better follow up questions",
                "Incorrect or unsupported information",
            ],
        )

        feedback_notes = st.text_area(
            "Optional feedback notes",
            placeholder="What should the system improve?",
        )

        if st.button("Save Feedback"):
            if feedback_choice == "Select feedback":
                st.warning("Please select a feedback option first.")
            else:
                feedback_path = save_feedback(feedback_choice, feedback_notes)
                st.success(f"Feedback saved to: {feedback_path}")


st.divider()

st.header("Draft Agentic System Design")

st.markdown(
    """
TrendLens AI currently uses one main TrendLens Analysis Agent.

The agent follows a structured workflow:
Source Intake, Source Normalization, Source Comparison, Trend Extraction, Risk and Impact Assessment, Confidence Assessment, and Report Generation.

Future versions could split these steps into separate autonomous agents and add background monitoring for developing public events.
"""
)