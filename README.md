# TrendLens AI

TrendLens AI is an agentic situational awareness and event analysis platform that turns public information into structured intelligence style reporting products.

The system helps users manage information overload by organizing local, national, and international public events into clear summaries, source comparisons, trend analysis, confidence notes, second and third order effects, and executive level briefing outputs.

TrendLens AI is a Project 2 working draft for an agentic artificial intelligence system. The current build focuses on public source analysis, structured reporting workflows, a real model callable tool, saved outputs, feedback logging, evaluation records, and a planned semi automated monitoring workflow.

The system does not replace professional judgment. It supports analysis by organizing public information, identifying patterns, highlighting information gaps, and helping users review what changed during developing events.

## Project 2 Working Draft Checkpoint

This repository is a working draft submission for Project 2.

Project 2 focuses on agentic systems. The goal is to design and ship an artificial intelligence workflow that can use tools, support Model Context Protocol style concepts, route tasks through different model behaviors, and operate with more autonomy than a basic chatbot.

TrendLens AI demonstrates progress through:

1. A working Streamlit interface.
2. Public source intake.
3. Target audience selection.
4. Report purpose input.
5. Role based report customization.
6. Structured prompt workflows.
7. One real model callable tool with a function schema.
8. Local helper functions for saving reports and feedback.
9. Report generation.
10. Report saving.
11. Feedback logging.
12. Evaluation logging.
13. Event history planning.
14. Semi automated monitoring design.
15. Prompt based routing design.
16. Model Context Protocol style tool structure.

The current version is not a final production system. It is a working prototype that shows a clear direction, working components, and continued development toward an agentic workflow.

## Instructor Feedback Addressed

This README was updated to directly address the Project 2 feedback.

The feedback identified four needed fixes:

1. The app had helper functions, but the model was not actually calling a tool.
2. The routing layer changed prompts, but it did not truly route to different models.
3. The deployed app was asleep and needed to be opened and verified.
4. The project needed an evaluation record showing expected versus actual output.

The revised project documentation addresses those items as follows:

1. Tool use is now defined as a real model callable tool named `analyze_public_sources`.
2. Routing is described honestly as prompt based routing unless a second model is later configured.
3. Deployment status is tracked as a required manual check before final submission.
4. Evaluation results are documented in `Tests/eval_results.md`.

## Live Demo and Deployment Status

Live app link:

```text
Add Streamlit deployed app link here
```

Deployment note:

Some free hosted Streamlit apps may sleep after inactivity. Before submitting the project, the deployed app should be opened, awakened, and tested with one sample input. The result should be recorded in `BUILD_LOG.md`.

Recommended deployment check entry:

```text
02JUN2026: Opened the deployed TrendLens AI app after inactivity. Confirmed the app loaded, accepted public source input, generated a structured situational awareness report, and allowed the output to be saved. Added an evaluation record with expected versus actual output.
```

## Project Goal

The goal of TrendLens AI is to build an AI assisted workflow system that goes beyond simple article summarization by introducing:

1. Reasoning based event categorization.
2. Structured reporting workflows.
3. Trend and pattern analysis.
4. Source comparison.
5. Confidence assessment.
6. Adaptive report generation.
7. Analyst style briefing products.
8. Significant activity tracking.
9. Raw tracker generation.
10. Follow up question and Request for Information generation.
11. Semi automated update monitoring.
12. Prompt based routing for different user needs.
13. Real model callable tool use.

TrendLens AI is inspired by real world operational analysis workflows where large amounts of rapidly changing information must be converted into meaningful situational awareness products.

## Problem Statement

During developing events, public information changes quickly. Multiple sources may report different details, update at different times, or focus on different parts of the event. This can make it difficult for users to understand what happened, why it matters, what changed, what is confirmed, what is uncertain, and what questions still need to be answered.

A basic chatbot can summarize pasted text, but it does not always guide the user through a repeatable analysis process. TrendLens AI adds structure by asking for the target audience, report purpose, source information, source type, report sections, and output style. The system then uses a model callable source analysis tool and prompt guided reasoning to produce a consistent situational awareness report.

## Narrow Project Scope

TrendLens AI has a narrow and realistic scope for this working draft.

The current version focuses on:

1. Public information only.
2. User pasted source text.
3. Two to three public sources per report.
4. Local, national, and international public events.
5. Role based report generation.
6. Intelligence style situational awareness summaries.
7. Source comparison and reliability notes.
8. Confidence assessment.
9. Follow up questions and Requests for Information.
10. Saved report outputs.
11. Feedback logging.
12. One model callable source analysis tool.
13. Semi automated monitoring design.
14. Prompt based routing design.
15. Model Context Protocol style tool planning.

This version does not collect classified, private, restricted, sensitive, or protected information. Users should only enter public or synthetic information.

## Target Audience

The primary target audience is the intelligence analyst.

TrendLens AI is also designed to support:

1. Emergency management personnel.
2. Emergency responders.
3. Researchers.
4. Journalists.
5. Security professionals.
6. Students.
7. Organizations requiring situational awareness.
8. Members of the public seeking clear event summaries.

## Primary Audience

Intelligence analysts can use TrendLens AI to organize public reporting, compare source details, identify emerging trends, assess confidence, and prepare briefing style outputs.

## Secondary Audience

Emergency management personnel and emergency responders can use TrendLens AI to quickly understand public safety updates, local incident reporting, weather effects, infrastructure issues, and community impact concerns.

## Public Audience

Members of the public can use TrendLens AI to better understand developing events without needing to write advanced prompts or manually compare multiple sources.

## Value Beyond a Basic Chatbot

TrendLens AI is more than a basic chat box because it gives the user a repeatable workflow.

The application guides the user through:

1. Defining the target audience.
2. Defining the report purpose.
3. Entering public source text.
4. Labeling source type.
5. Selecting desired report sections.
6. Allowing the model to call a source analysis tool.
7. Comparing public source information.
8. Identifying confidence level.
9. Generating a structured situational awareness report.
10. Saving the report output.
11. Saving user feedback.
12. Preparing for future monitoring updates.

The user does not need to know how to write a strong intelligence prompt. The application handles the structure and produces a consistent report format.

## Core Features

Current and planned capabilities include:

1. Public event ingestion.
2. Significant activity tracking.
3. Structured event categorization.
4. Trend and anomaly detection.
5. Trend and pattern analysis.
6. Executive style briefing generation.
7. Raw tracker generation.
8. Follow up question generation.
9. Request for Information generation.
10. Multi level reporting outputs.
11. Event history and contextual memory.
12. Analyst workflow automation.
13. Public source comparison.
14. Confidence assessment.
15. Second and third order effects.
16. Saved report outputs.
17. Feedback logging.
18. Semi automated monitoring.
19. Prompt based routing.
20. Model callable tool use.
21. Model Context Protocol style tool design.

## Example Workflow

1. User submits public information.

Examples include:

News article  
Event summary  
Incident description  
Public information update  
Public safety alert  
Weather statement  
Government update  

2. The model receives the tool schema.

The model is given access to the `analyze_public_sources` tool. This tool is used when the report requires source comparison, confidence assessment, or identification of information gaps.

3. The model calls the tool when needed.

The model sends structured arguments to the tool, including source text, source labels, target audience, and report purpose.

4. The application executes the tool.

The app runs the local Python function and returns a structured result to the model.

5. The model generates the final report.

The model uses the returned tool result to write the final situational awareness product.

6. User reviews the output.

The user can save the report, provide feedback, and use the output as a draft for further review.

## Real Model Callable Tool Use

The first version of the app used helper functions that were called directly by the Streamlit application. Those helper functions were useful for app logic, but they did not fully satisfy the tool use requirement because the model itself was not deciding when to call a tool.

The revised design defines one real model callable tool:

```text
analyze_public_sources
```

This tool allows the model to request structured source analysis before writing the final report.

### Purpose of the Tool

The `analyze_public_sources` tool compares pasted public sources and returns structured analysis that the model can use to generate the final report.

The tool is responsible for identifying:

1. Source count.
2. Main event topic.
3. Event type.
4. Location.
5. Key confirmed facts.
6. Shared details across sources.
7. Conflicting details across sources.
8. Missing information.
9. Possible public safety impacts.
10. Possible operational impacts.
11. Possible second and third order effects.
12. Confidence level.
13. Recommended follow up questions.
14. Recommended Requests for Information.

### Function Schema Example

```json
{
  "type": "function",
  "name": "analyze_public_sources",
  "description": "Compare public event sources and return structured source analysis before the final situational awareness report is written.",
  "parameters": {
    "type": "object",
    "properties": {
      "sources": {
        "type": "array",
        "description": "Public source entries submitted by the user.",
        "items": {
          "type": "object",
          "properties": {
            "label": {
              "type": "string",
              "description": "Short label for the source, such as local news, city alert, or industry report."
            },
            "source_type": {
              "type": "string",
              "description": "Type of source, such as article, public safety alert, weather statement, government update, or report."
            },
            "text": {
              "type": "string",
              "description": "Public or synthetic source text pasted by the user."
            }
          },
          "required": ["label", "source_type", "text"]
        }
      },
      "target_audience": {
        "type": "string",
        "description": "Selected audience, such as Intelligence Analyst, Emergency Responder, or Public Audience."
      },
      "report_purpose": {
        "type": "string",
        "description": "The user's stated purpose for the report."
      }
    },
    "required": ["sources", "target_audience", "report_purpose"]
  }
}
```

### Tool Call Workflow

The intended tool call workflow is:

1. User enters public source text.
2. App sends the model the report request and the `analyze_public_sources` tool schema.
3. Model decides whether source analysis is needed.
4. Model calls `analyze_public_sources` with structured arguments.
5. App executes the Python function in `trend_tools.py`.
6. App returns the tool output to the model.
7. Model uses the tool output to write the final report.
8. App displays the final report in Streamlit.
9. User can save the report and provide feedback.

### Why This Counts as Tool Use

This is different from normal helper functions because the model receives the tool definition and chooses to call it as part of the workflow. The application then executes the function and gives the result back to the model. This creates a model tool loop instead of only using backend Python functions.

## Local Helper Functions

TrendLens AI also uses local helper functions for normal app behavior.

Examples include:

1. Saving generated reports.
2. Saving user feedback.
3. Saving monitoring topics.
4. Comparing previous source text against updated source text.
5. Recording evaluation results.

These helper functions are still useful, but they are separate from the model callable tool. The README separates these two categories so the project does not overstate what the model is doing.

## Agentic System Design

This project focuses on the core pillars of agentic AI systems:

1. Reasoning.
2. Memory.
3. Tools.
4. Feedback.
5. Limited autonomy.
6. Prompt based routing.
7. Model Context Protocol style structure.

## Reasoning

The system evaluates event significance, categorizes activity, compares source details, identifies information gaps, and generates structured outputs.

Reasoning tasks include:

1. Event categorization.
2. Source comparison.
3. Trend identification.
4. Pattern recognition.
5. Anomaly detection.
6. Confidence assessment.
7. Risk identification.
8. Second and third order effect analysis.
9. Follow up question generation.
10. Request for Information generation.

## Memory

The system is designed to maintain contextual awareness of prior events and trends.

Current and planned memory functions include:

1. Saving generated reports.
2. Saving user feedback.
3. Saving monitored topics.
4. Saving prior source text.
5. Comparing old and new source text.
6. Building event history over time.

This memory design helps the application support continuity across event updates.

## Tools

TrendLens AI uses two types of tools.

### Model Callable Tool

The model callable tool is:

```text
analyze_public_sources
```

This tool is exposed to the model through a function schema. The model can call it before generating the final report.

### Application Helper Tools

The application also uses helper functions for app workflow support.

Helper tools include:

1. Report saving.
2. Feedback saving.
3. Source change detection.
4. Monitoring topic storage.
5. Scheduled monitoring checks.
6. Evaluation logging.

The goal is to show that the application can take structured actions inside a workflow, while also showing at least one real model callable tool.

## Feedback

User corrections and iterative evaluation improve workflow consistency and output quality.

Feedback may include:

1. Whether the report was useful.
2. Whether the report stayed grounded in the source text.
3. Whether the confidence level made sense.
4. Whether the selected report sections were helpful.
5. Whether the report tone matched the selected audience.
6. Whether the system missed important details.

Feedback is stored so future versions can compare report quality over time.

## Limited Autonomy

TrendLens AI includes a planned semi automated monitoring workflow.

A user can enter a public topic or event. The system can then check for updated information every five hours. When meaningful changes are detected, the system can generate an updated situational awareness report for human review.

This is semi automated because the user still chooses the topic, reviews the final report, and validates the information.

## Weeks 3 to 4 Agentic Workflow Requirement

The Weeks 3 to 4 project focus is to design and ship an agentic workflow using tools, Model Context Protocol, and model routing.

TrendLens AI addresses this requirement through:

1. A guided Streamlit workflow.
2. A model callable function tool.
3. Structured public source analysis.
4. Prompt based routing by audience and task type.
5. Saved reports.
6. Feedback logging.
7. Evaluation records.
8. Planned monitoring checks.
9. MCP style separation of prompts, tools, context, saved state, and outputs.

## Agentic Workflow

The current workflow is:

1. User enters a public event topic or public source text.
2. The application validates whether enough source text is present.
3. The application sends the source text, user role, and report purpose to the model.
4. The model can call `analyze_public_sources`.
5. The application executes the tool call and returns the structured tool output.
6. The model uses the tool output to produce a situational awareness report.
7. The application displays the report.
8. The save report helper stores the output.
9. The feedback helper stores the user evaluation.
10. The monitoring helper can compare prior source text against updated source text in a planned workflow.
11. The scheduler worker can check for updates every five hours in a planned workflow.
12. The routing layer selects the correct prompt behavior for the task.

## Tool Layer Design

TrendLens AI separates major actions into clear functions.

The current and planned tool layer includes:

1. Model callable source analysis tool.
2. Report saving helper.
3. Feedback saving helper.
4. Source change detection helper.
5. Monitoring topic helper.
6. Scheduler worker helper.
7. Prompt routing helper.
8. Evaluation logging helper.

This structure makes the application easier to test, expand, and evaluate.

## Model Context Protocol Style Design

Model Context Protocol, also known as MCP, is a design approach for connecting AI systems to tools, context, data, and structured actions.

TrendLens AI does not require a full production MCP server for this working draft. Instead, the project uses an MCP style architecture by separating tools, inputs, outputs, prompts, context, and saved state into clear components.

The MCP style design includes:

1. Clearly defined user inputs.
2. Structured public source text.
3. Separate prompt files.
4. One model callable tool schema.
5. Local helper functions.
6. Saved report outputs.
7. Saved feedback.
8. Monitoring state files.
9. Scheduled update check planning.
10. Routing logic for different task types.

Future versions could convert these local tools into a formal MCP server or MCP compatible tool layer.

## Routing Design

TrendLens AI uses prompt based routing in the current working draft.

This means the app changes the instruction path based on the selected user role and task type, but it does not claim to route to completely separate models unless the code is later configured to do so.

This clarification is important because changing prompts is not the same thing as using different models.

## Current Routing Behavior

The current routing layer uses task type and audience selection.

Example routing logic:

1. If the user selects Intelligence Analyst, the system uses an intelligence style report prompt.
2. If the user selects Emergency Responder, the system uses a public safety impact prompt.
3. If the user selects Public Audience, the system uses a plain language explanation prompt.
4. If the task is monitoring, the system uses a change detection prompt.
5. If the task is feedback evaluation, the system uses a quality review prompt.

This approach keeps the prototype simpler, cheaper, and easier to evaluate while still showing how different analyst workflows can produce different report structures.

## Future Multi Model Routing Option

A future version could use true multi model routing.

Example future routing plan:

1. A smaller or faster model could triage the source text.
2. A stronger model could generate the final intelligence style report.
3. A separate evaluation model could compare expected versus actual output.
4. A monitoring model could summarize changes between old and new source text.

The current version should be graded as prompt based routing, not true multi model routing.

## Semi Automated Monitoring Concept

TrendLens AI includes a planned semi automated monitoring workflow.

The goal is to allow a user to enter a specific public topic or event. The system will then check for updated public source text on a regular interval and generate an updated situational awareness product when new information is available.

For this project version, the planned monitoring interval is every five hours.

The semi automated workflow is designed to:

1. Store the user selected monitoring topic.
2. Track the last reviewed public source text.
3. Check for updated information every five hours.
4. Compare new text against prior text.
5. Identify what changed.
6. Decide whether the change is meaningful.
7. Generate an updated report when needed.
8. Save the updated output.
9. Present the output for human review.

## What Counts as a Meaningful Change

A meaningful change may include:

1. New confirmed location.
2. New official statement.
3. New casualty or damage information.
4. New infrastructure impact.
5. New public safety guidance.
6. New actor or organization involved.
7. New timeline detail.
8. New contradiction between sources.
9. New second or third order effect.
10. Change in confidence level.

## Report Output Sections

TrendLens AI can generate report sections such as:

1. Bottom Line Up Front.
2. Executive summary.
3. Source overview.
4. Key facts.
5. Timeline.
6. Source comparison and reliability notes.
7. What changed.
8. So what or why this matters.
9. Operational impacts.
10. Public safety impacts.
11. Second and third order effects.
12. Confidence assessment.
13. Information gaps.
14. Recommended follow up questions.
15. Requests for Information.
16. Forty five second brief.

## Example Use Case

Example topic:

```text
Chemical spill at an aerospace supplier facility
```

Example target audience:

```text
Intelligence Analyst
```

Example report purpose:

```text
Prepare a commander update on a developing public event.
```

Example sources:

```text
Source 1: Local news article describing a chemical spill.
Source 2: Public safety update describing evacuation guidance and road closures.
Source 3: Industry article explaining the supplier role in aerospace manufacturing.
```

Expected output:

The report should identify confirmed facts, compare the sources, explain public safety effects, identify possible supply chain concerns, identify information gaps, and generate follow up questions. The report should avoid classified claims, avoid unsupported assumptions, and clearly separate confirmed details from possible impacts.

## Evaluation

Evaluation records are stored in:

```text
Tests/eval_results.md
```

### Evaluation Record 1 Summary

Test purpose:

Confirm TrendLens AI can compare multiple public event sources and generate a structured intelligence style report.

Expected output:

The report should include a Bottom Line Up Front, executive summary, key facts, source comparison, operational impacts, second and third order effects, confidence level, information gaps, and follow up questions.

Actual output:

TrendLens AI generated a structured report with a Bottom Line Up Front, executive summary, key trends, risks, confidence level, and follow up questions. The output identified public safety impacts, possible supply chain concerns, and information gaps. The output needed minor improvement in clearly labeling which details came from each source.

Result:

Mostly successful.

Revision made:

Added a real model callable tool called `analyze_public_sources` so the model can request source comparison before producing the final report. Updated the README to explain that routing is prompt based rather than true multi model routing.

## Grounding and Safety Rules

TrendLens AI should follow these rules:

1. Use only public or synthetic information.
2. Do not ask for classified, private, restricted, sensitive, or protected information.
3. Do not invent facts that are not present in the sources.
4. Separate confirmed facts from possible impacts.
5. Identify source gaps and uncertainty.
6. Include confidence levels when appropriate.
7. Keep the final report as a draft for human review.
8. Avoid presenting public source analysis as official intelligence.
9. Avoid operational recommendations that require authority or professional judgment.
10. Encourage users to verify important details with official sources.

## Technologies

TrendLens AI uses:

Python  
Streamlit  
OpenAI API  
Pandas  
GitHub  
Prompt engineering workflows  
Markdown  
File based output logging  
Prompt based routing logic  
Function schema tool design  
Model Context Protocol style tool design  

## Project Structure

The expected project structure is:

```text
TrendLens-AI/
    app.py
    trend_tools.py
    monitoring.py
    scheduler_worker.py
    README.md
    BUILD_LOG.md
    requirements.txt
    Prompts/
        system_prompt.md
        report_prompt.md
        routing_prompt.md
        monitoring_prompt.md
    Outputs/
        saved reports
    Tests/
        eval_results.md
        test input examples
    Monitoring/
        monitored_topics.json
        last_source_text.json
        monitoring_log.md
```

## Main Files

`app.py`

Runs the Streamlit application, collects user inputs, displays generated reports, exposes the model callable tool schema, handles tool call responses, and connects the app interface to helper functions.

`trend_tools.py`

Stores reusable Python functions such as `analyze_public_sources`, `save_report`, `save_feedback`, and other report support functions.

`monitoring.py`

Stores monitoring related functions such as topic storage, source comparison, and meaningful change detection.

`scheduler_worker.py`

Represents the planned scheduled workflow that can check monitored topics every five hours.

`Tests/eval_results.md`

Stores expected versus actual output records.

`BUILD_LOG.md`

Documents project changes, testing, fixes, and deployment checks.

## How to Run Locally

1. Clone the repository.

```bash
git clone your-repository-url
cd TrendLens-AI
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Add the API key as an environment variable.

```bash
set OPENAI_API_KEY=your_api_key_here
```

For PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

4. Run the Streamlit app.

```bash
streamlit run app.py
```

5. Open the local URL shown in the terminal.

## How to Use the App

1. Select the target audience.
2. Enter the report purpose.
3. Paste two or three public source texts.
4. Label each source.
5. Select desired report sections.
6. Generate the report.
7. Review the output.
8. Save the report if useful.
9. Submit feedback.
10. Record evaluation notes when testing.

## Current Limitations

The current version has limitations:

1. It relies on user pasted source text.
2. It does not independently verify every claim.
3. It is not connected to live official feeds in the working draft.
4. It uses prompt based routing rather than confirmed multi model routing.
5. It includes planned monitoring features that may still need final testing.
6. It should not be used with classified, private, restricted, sensitive, or protected information.
7. It produces draft analysis for human review, not official reporting.

## Future Improvements

Future versions could add:

1. True multi model routing.
2. A formal MCP server.
3. Live public source connectors.
4. Source credibility scoring.
5. Better change detection.
6. Automated evaluation tests.
7. Dashboard style event history.
8. Export to PDF or Word.
9. Map based event visualization.
10. More role specific report templates.
11. Better confidence scoring.
12. More transparent source attribution.

## Submission Checklist

Before final submission:

1. Confirm `app.py` includes the model callable tool schema.
2. Confirm `trend_tools.py` includes `analyze_public_sources`.
3. Confirm README explains tool use clearly.
4. Confirm README explains routing honestly as prompt based routing.
5. Open the deployed app and wake it if it is asleep.
6. Run one test input in the deployed app.
7. Save or screenshot the successful output.
8. Add one record to `Tests/eval_results.md`.
9. Add one deployment check entry to `BUILD_LOG.md`.
10. Commit and push the final changes.

Recommended commit message:

```text
Add model callable tool and evaluation record
```

## Originality and Ownership

TrendLens AI was designed as an original Project 2 prototype focused on public event analysis, situational awareness reporting, and analyst workflow support. The concept, workflow design, audience framing, report structure, and project scope were developed for this course project.

The project reflects an applied use case for agentic AI in public source analysis. It is intentionally scoped to public or synthetic information and does not require classified or restricted data.

## Final Project Summary

TrendLens AI is an agentic public event analysis assistant that helps users turn multiple public sources into one structured situational awareness report.

The most important update is that the system now includes a real model callable tool, `analyze_public_sources`, instead of only using helper functions called directly by the app. The README also clarifies that routing is currently prompt based routing, not true multi model routing, unless future code adds a second model. The project now includes a clearer deployment check process and an evaluation record showing expected versus actual output.
