# TrendLens AI Evaluation Results

## Evaluation Purpose

The purpose of this evaluation is to test whether TrendLens AI provides value beyond a basic chatbot summary. The application should take public information style inputs, organize them into a structured situational awareness product, identify key patterns, explain significance, assess confidence, and generate follow up questions.

This evaluation also checks whether TrendLens AI demonstrates Project 2 agentic system behavior through reasoning, tool use, memory, feedback, model routing, and semi automated monitoring.

## Evaluation Criteria

The system will be evaluated on whether it can:

1. Identify the main event type.
2. Extract or acknowledge missing dates, locations, and actors.
3. Combine multiple sources into one unified report.
4. Generate a clear Bottom Line Up Front.
5. Explain the so what.
6. Identify trends or patterns.
7. Identify risks or concerns.
8. Provide a reasonable confidence level.
9. Generate useful follow up questions.
10. Produce a short 45 second brief.
11. Route the output based on the selected audience.
12. Save or download generated reports.
13. Save user feedback.
14. Compare previous source text against updated source text.
15. Support the five hour monitoring workflow design.

## Test Case 1: International Security and Diplomatic Tension

### Input Sources

Source 1: Synthetic UAS incident involving Atropia and Ariana.

Source 2: Synthetic peace talks involving Limaria, Farnovia, nuclear program oversight, and chemical weapons storage regulations.

### Role

Intelligence Analyst

### Task Type

Generate situational awareness report

### Expected Behavior

The system should identify the first source as a security related incident involving UAS activity, government facilities, and possible escalation. The system should identify the second source as a diplomatic and arms control related event. The system should connect both sources under broader themes of regional security, escalation management, government response, and uncertainty without inventing unsupported facts.

### Actual Output

Pending live app test with these exact synthetic sources.

### Pass or Needs Improvement

Pending.

### Notes for Improvement

This test should be completed before final submission. It is useful because it tests whether TrendLens AI can compare two related but different international security sources without overstating the connection.

## Test Case 2: Natural Disaster and Humanitarian Response

### Input Sources

Source 1: Synthetic wildfire event in Philconia involving displaced residents, FEMA, firefighters, and animal rescue support.

### Role

Emergency Responder

### Task Type

Generate situational awareness report

### Expected Behavior

The system should identify the event as a natural disaster and humanitarian response issue. It should recognize public safety, displacement, emergency response, animal rescue, and possible infrastructure strain as relevant concerns. Because only one source is provided, the report should state that source comparison is limited.

### Actual Output

Pending live app test with this exact synthetic source.

### Pass or Needs Improvement

Pending.

### Notes for Improvement

This test should be completed before final submission. It is useful because it tests whether the app adjusts tone and focus for an emergency responder audience.

## Test Case 3: Food Security and Economic Development

### Input Sources

Source 1: Synthetic Drasta company report about the Susu crop, low cost farming tools, irrigation training, and employment growth.

### Role

Researcher or Student

### Task Type

Identify trends and anomalies

### Expected Behavior

The system should identify the event as a food security, economic development, and agricultural innovation issue. It should recognize potential impacts on remote communities, workforce development, farming practices, food access, and supply chain resilience. It should avoid making claims beyond the source text.

### Actual Output

Pending live app test with this exact synthetic source.

### Pass or Needs Improvement

Pending.

### Notes for Improvement

This test should be completed before final submission. It is useful because it tests trend analysis outside a public safety or military style topic.

## Test Case 4: Mixed Event Inputs

### Input Sources

Source 1: Synthetic UAS incident in Atropia.

Source 2: Synthetic wildfire response in Philconia.

Source 3: Synthetic Drasta Susu crop development report.

### Role

Intelligence Analyst

### Task Type

Compare public sources

### Expected Behavior

The system should avoid forcing unrelated events into one false narrative. It should identify that the sources represent separate event categories while still producing a structured overview. It should separate security, disaster response, and food security themes clearly.

### Actual Output

Pending live app test with these exact synthetic sources.

### Pass or Needs Improvement

Pending.

### Notes for Improvement

This test should be completed before final submission. It is important because it checks whether the app avoids false connections between unrelated inputs.

## Test Case 5: Public Weather Source and Executive Briefing

### Input Sources

Source 1: Public weather article about clear skies giving Metro Detroit good Blue Moon viewing conditions. The source included information about clear and dry weather, sunset timing, the Blue Moon, micromoon conditions, planetary alignment, and temperatures falling from near 60 degrees to the low 40s or near 50 overnight.

### Role

Intelligence Analyst

### Task Type

Create executive briefing

### Report Purpose

Brief weather patterns seen in Michigan and illumination, along with information from the article, to command.

### Selected Sections

1. Source Overview
2. Bottom Line Up Front
3. Executive Summary
4. So What or Why This Matters
5. Source Comparison and Reliability Notes
6. Confidence Assessment
7. Follow Up Questions or RFIs
8. Forty Five Second Brief

### Expected Behavior

The system should identify the source as a weather and public observation event. It should summarize clear sky conditions, Blue Moon viewing, temperature trends, and public activity considerations. Since only one source is provided, the report should acknowledge limited source comparison. It should tailor the output to an intelligence analyst or command audience.

### Actual Output

The deployed app generated a full TrendLens AI report titled:

Clear Skies Enable Optimal Blue Moon Viewing in Metro Detroit, Michigan, Late May 2026

The output included:

1. Source Overview
2. Bottom Line Up Front
3. Executive Summary
4. Five Ws
5. So What or Why This Matters
6. Source Comparison and Reliability Notes
7. Confidence Assessment
8. Follow Up Questions or RFIs
9. Forty Five Second Brief

The report correctly identified the event as clear and dry weather supporting Blue Moon viewing in Metro Detroit. It explained that the event could increase outdoor activity at night and may matter for public safety, traffic, public gatherings, and command awareness.

### Pass or Needs Improvement

Pass.

### Notes for Improvement

The report was useful and structured. The confidence assessment was high even though only one source was used. In future testing, the confidence language should more clearly balance source credibility with the limitation that there was only one source.

## Test Case 6: Local Tool Test with Chemical Spill Scenario

### Input Sources

Source 1: Public safety alert stating that city officials reported a chemical spill near an industrial facility and roads near the facility were closed while crews assessed the scene.

Source 2: News article stating that fire officials confirmed nearby businesses were evacuated as a precaution and the county emergency management office told the public to avoid the area.

### Role

Intelligence Analyst

### Task Type

Generate situational awareness report

### Expected Behavior

The system should identify the event as a public safety and hazardous materials incident. It should recognize road closures, precautionary evacuations, public guidance, and missing details such as the chemical type, exact location, scale, injuries, and cleanup status.

### Actual Output

The local trend_tools.py test generated a complete TrendLens AI report. The report included:

1. Source Overview
2. Bottom Line Up Front
3. Executive Summary
4. Source Comparison and Reliability Notes
5. Confidence Assessment
6. Recommended Follow Up Questions

The output correctly identified the chemical spill, road closures, evacuations, and public advisory. It also identified missing details such as the chemical involved, exact location, contamination extent, health impacts, and cleanup status.

### Pass or Needs Improvement

Pass.

### Notes for Improvement

The output demonstrated that the report generation tool works outside the Streamlit interface. This is useful because it confirms that trend_tools.py can operate as a separate tool layer in the agentic system.

## Test Case 7: Monitoring Workflow Old Versus New Source Text

### Input Sources

Previous source text:

City officials reported a chemical spill near an industrial facility. Roads near the facility were closed while crews assessed the scene.

Updated source text:

City officials reported a chemical spill near an industrial facility. Roads near the facility were closed while crews assessed the scene. Fire officials confirmed that two nearby businesses were evacuated as a precaution. The county emergency management office issued public guidance to avoid the area.

### Role

Not applicable. This test evaluated the monitoring tool.

### Task Type

Manual change detection

### Expected Behavior

The system should compare the previous source text against the updated source text. It should identify that the updated source includes new information about evacuations and public guidance. The output should show that a change occurred and should mark the change as meaningful.

### Actual Output

The monitoring workflow successfully compared the previous and updated source text. The tool identified that the updated source text added new information and categorized the change as meaningful.

### Pass or Needs Improvement

Pass.

### Notes for Improvement

The current monitoring output is useful but can be made more user friendly. A future version should display old versus new information in a cleaner summary instead of relying mainly on JSON output.

## Test Case 8: Scheduler Worker Status Test

### Input Sources

No source text was used. This test checked the scheduler worker command line status function.

### Command Tested

python scheduler_worker.py --status

### Expected Behavior

The scheduler should print a status summary showing the number of monitoring topics, due topics, due topic names, default check interval, scheduler status file path, and monitoring log file path.

### Actual Output

The scheduler returned a JSON status showing:

1. total_topics: 0
2. due_topics: 0
3. due_topic_names: empty list
4. default_check_interval_hours: 5
5. scheduler_status_file: Monitoring/scheduler_status.json
6. monitoring_log_file: Monitoring/monitoring_log.md

### Pass or Needs Improvement

Pass.

### Notes for Improvement

The result was correct because no monitoring topics had been saved yet. This test proves the scheduler worker can run and report status without crashing.

## Test Case 9: Scheduler Worker Scan Once Test

### Input Sources

No source text was used. This test checked whether the scheduler worker could complete a one time scan.

### Command Tested

python scheduler_worker.py --scan-once

### Expected Behavior

The scheduler should scan for monitoring topics due for review and return a structured result. If no topics exist, it should return zero due topics without crashing.

### Actual Output

The scheduler returned:

1. due_topic_count: 0
2. results: empty list

### Pass or Needs Improvement

Pass.

### Notes for Improvement

The result was correct because no monitoring topics were saved at the time of the scan. A future test should save a monitoring topic first, then run the scheduler after the topic becomes due.

## Test Case 10: Deployed App Interface Test

### Input Sources

No report source text was used. This test checked whether the deployed Streamlit interface loaded.

### Expected Behavior

The deployed app should open from the Streamlit Community Cloud link and display:

1. TrendLens AI title
2. Generate Report tab
3. Monitoring Workflow tab
4. About tab
5. Source input fields
6. Report section selector
7. Agent workflow preview
8. Generate report button

### Actual Output

The deployed app loaded successfully after the main file path was corrected to app.py. The interface displayed the expected title, description, tabs, source input fields, report section selector, and Agent Workflow Preview panel.

### Pass or Needs Improvement

Pass.

### Notes for Improvement

The first deployment attempt pointed to monitoring.py, which caused the app to appear blank. This was corrected by changing the main file path to app.py.

## Initial Evaluation Summary

TrendLens AI is meeting the working draft goal for Project 2. The app demonstrates meaningful progress and includes working components. It is not only a chatbot because it guides the user through a structured workflow, routes the output based on audience and task type, generates structured reports, saves reports, logs feedback, and includes monitoring tools for old versus new source comparison.

The strongest working features are:

1. Clear Streamlit interface.
2. Public source intake.
3. Role based report generation.
4. Report section selection.
5. Agent workflow preview.
6. Model routing display.
7. Structured report generation.
8. Report download.
9. Report saving.
10. Feedback logging.
11. Monitoring workflow tab.
12. Old versus new source comparison.
13. Scheduler worker support.
14. Streamlit Community Cloud deployment.

The current draft still needs more final evaluation examples using the original synthetic test cases. However, the deployed weather test, chemical spill tool test, monitoring test, and scheduler tests show that the core system is working.

## Prompt or Design Changes Made After Testing

The following design changes were made or identified after testing:

1. The README was updated to separate working features from planned features.
2. The project scope was narrowed to public source situational awareness reporting.
3. The primary audience was clarified as intelligence analysts.
4. Secondary audiences were clarified as emergency responders and the public.
5. app.py was updated to show the agent workflow inside the user interface.
6. monitoring.py was added to support old versus new source text comparison.
7. scheduler_worker.py was added to support timed monitoring checks.
8. trend_tools.py was merged with the original file to preserve source cleaning, URL extraction, prompt loading, source consolidation, report generation, saving, and feedback features.
9. The deployed Streamlit app was corrected to use app.py instead of monitoring.py.
10. Future design should add clearer old versus new change summaries in the Monitoring Workflow tab.
11. Future design should let the user choose check frequency in minutes or hours.
12. Future design should use persistent storage if user history, saved monitoring topics, or email alerts are added.
13. Future design should use an external background worker or cloud scheduler for true always running monitoring.

## Overall Result

Overall result: Pass for working draft.

TrendLens AI demonstrates meaningful progress toward an agentic system. The current version includes a working deployed app, structured report generation, tool based helper functions, model routing, saved outputs, feedback logging, monitoring support, and scheduler worker logic. The final version should add more evaluation outputs, improve monitoring display, and document any remaining limitations clearly.