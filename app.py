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
    """
    Creates one source input section and returns the source information.
    """
    st.subheader(f"Source {source_number}")

    if required:
        st.caption("Required source")
    else:
        st.caption("Optional source")

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
        "label": source_label,
        "url": source_url,
        "text": source_text,
    }


st.title("TrendLens AI")
st.caption("Agentic public event analysis and situational awareness reporting assistant")

st.markdown(
    """
TrendLens AI transforms public information sources into one structured situational awareness product.

For this draft, paste one to three public article excerpts, news updates, public alerts, or event descriptions. The system combines them into an analyst style report with a Bottom Line Up Front, executive summary, so what, key trends, risks or concerns, confidence level, follow up questions, and a 45 second brief.
"""
)

st.info(
    "Use only public or synthetic information for this project. Do not paste classified, private, sensitive, or restricted information."
)

with st.sidebar:
    st.header("TrendLens Draft Scope")

    st.markdown(
        """
This draft demonstrates:

Reasoning: compares sources and identifies significance.

Memory: stores the latest report during the session.

Tools: uses helper functions for source cleaning, prompt routing, report generation, report saving, and feedback logging.

Feedback: saves user feedback for later evaluation.
"""
    )

    st.divider()

    if st.session_state.latest_report:
        st.success("A report has been generated in this session.")
    else:
        st.warning("No report generated yet.")

st.divider()

st.header("1. Add Public Information Sources")

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
valid_sources = [source for source in sources if source["text"].strip()]

st.divider()

st.header("2. Generate TrendLens Report")

st.write(
    "The report will combine the submitted sources into one structured product instead of producing a generic article summary."
)

st.caption(f"Valid sources detected: {len(valid_sources)}")

generate_button = st.button("Generate TrendLens Report", type="primary")

if generate_button:
    if len(valid_sources) < 1:
        st.warning("Please paste at least one public information source before generating a report.")
    else:
        with st.spinner("Analyzing sources and generating structured report..."):
            report = generate_trendlens_report(valid_sources)
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
    st.header("3. TrendLens AI Report")

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
        st.header("4. Agent Workflow Used")

        st.markdown(st.session_state.latest_agent_workflow)

        st.divider()
        st.header("5. Feedback")

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
Reasoning: The system compares submitted public sources, identifies what matters, and creates a unified report.

Memory: The current draft stores the latest report and workflow summary in Streamlit session state so they remain available during the session.

Tools: The system uses Python helper functions to clean source text, build structured prompts, call the OpenAI API, save reports, and log feedback.

Feedback: The user can rate report quality and save feedback for later evaluation.
"""
)