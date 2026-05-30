import streamlit as st

from trend_tools import generate_trendlens_report, save_report, save_feedback


st.set_page_config(
    page_title="TrendLens AI",
    page_icon="📊",
    layout="wide"
)


if "latest_report" not in st.session_state:
    st.session_state.latest_report = ""

if "latest_report_path" not in st.session_state:
    st.session_state.latest_report_path = ""


st.title("TrendLens AI")
st.caption("Agentic public event analysis and situational awareness reporting assistant")

st.markdown(
    """
TrendLens AI helps transform multiple public information sources into one structured situational awareness product.

For this draft, paste two or three public article excerpts, news updates, or event descriptions. The system will combine them into an analyst style report with a Bottom Line Up Front, executive summary, key trends, risks, confidence level, and follow up questions.
"""
)

st.divider()

st.header("1. Add Public Information Sources")

st.subheader("Source 1")
source_1_label = st.text_input("Source 1 label", placeholder="Example: Local news article, Reuters update, city alert")
source_1_url = st.text_input("Source 1 URL", placeholder="Optional URL or source link")
source_1_text = st.text_area("Paste Source 1 text", height=180)

st.subheader("Source 2")
source_2_label = st.text_input("Source 2 label", placeholder="Example: National article, official statement, press release")
source_2_url = st.text_input("Source 2 URL", placeholder="Optional URL or source link")
source_2_text = st.text_area("Paste Source 2 text", height=180)

st.subheader("Source 3")
source_3_label = st.text_input("Source 3 label", placeholder="Optional third source")
source_3_url = st.text_input("Source 3 URL", placeholder="Optional URL or source link")
source_3_text = st.text_area("Paste Source 3 text", height=180)

sources = [
    {
        "label": source_1_label,
        "url": source_1_url,
        "text": source_1_text
    },
    {
        "label": source_2_label,
        "url": source_2_url,
        "text": source_2_text
    },
    {
        "label": source_3_label,
        "url": source_3_url,
        "text": source_3_text
    }
]

valid_sources = [source for source in sources if source["text"].strip()]

st.divider()

st.header("2. Generate TrendLens Report")

st.write(
    "The report will combine the submitted sources into one structured product instead of summarizing each source separately."
)

generate_button = st.button("Generate TrendLens Report")

if generate_button:
    if len(valid_sources) < 1:
        st.warning("Please paste at least one public information source before generating a report.")
    else:
        with st.spinner("Analyzing sources and generating structured report..."):
            report = generate_trendlens_report(valid_sources)
            st.session_state.latest_report = report

            if not report.startswith("Error"):
                report_path = save_report(report)
                st.session_state.latest_report_path = report_path

if st.session_state.latest_report:
    st.divider()
    st.header("3. TrendLens AI Report")

    st.markdown(st.session_state.latest_report)

    if st.session_state.latest_report_path:
        st.success(f"Report saved locally to: {st.session_state.latest_report_path}")

    st.download_button(
        label="Download Report as Markdown",
        data=st.session_state.latest_report,
        file_name="trendlens_report.md",
        mime="text/markdown"
    )

    st.divider()
    st.header("4. Feedback")

    feedback_choice = st.selectbox(
        "How useful was this report?",
        [
            "Select feedback",
            "Useful and specific",
            "Too broad",
            "Missing important context",
            "Needs clearer trends",
            "Needs better follow up questions"
        ]
    )

    feedback_notes = st.text_area(
        "Optional feedback notes",
        placeholder="What should the system improve?"
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

Memory: The current draft stores the latest report in Streamlit session state so it remains available during the session.

Tools: The system uses Python helper functions to clean source text, build structured prompts, call the OpenAI API, save reports, and log feedback.

Feedback: The user can rate the report quality and save feedback for later evaluation.
"""
)