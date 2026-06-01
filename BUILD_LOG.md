# TrendLens AI Build Log

This build log documents the development process for TrendLens AI during the Project 2 working draft period. The purpose of this file is to show what changed, why it changed, what was tested, what issues came up, and what still needs improvement.

## Project Summary

TrendLens AI is an agentic public event analysis and situational awareness reporting assistant. The application helps users turn public source text into structured intelligence style reports. The working draft focuses on source intake, role based report generation, selected report sections, model routing, report saving, feedback logging, and a semi automated monitoring workflow.

The main goal for this build was to move the project beyond a basic chatbot by creating a guided workflow with visible agentic behavior. The app now supports reasoning across source text, tool based actions, memory through saved files, feedback logging, and limited autonomy through monitoring and scheduled checks.

## Week Summary

This week focused on turning TrendLens AI from a project idea into a working deployed draft. The biggest development tasks were narrowing the scope, updating the README, rebuilding app.py, adding monitoring.py, adding scheduler_worker.py, updating trend_tools.py, testing report generation, and deploying the app through Streamlit Community Cloud.

The main lesson from the week was that the project needed to be honest about what is currently working versus what is planned. ChatGPT pushed back during prompt design and documentation planning by pointing out where the README claimed more than the deployed app showed. That feedback helped close the gap between the documentation and the working application.

## May 27, 2026

### Work Completed

1. Continued refining the Project 2 idea.
2. Focused the concept around public event analysis and situational awareness.
3. Identified the main problem as information overload during developing public events.
4. Began narrowing the app away from a broad event monitoring concept and toward a realistic source analysis workflow.
5. Discussed the need for the project to show more than basic summarization.

### Why This Mattered

The original concept was too broad. It included local, national, and international events, trend analysis, automation, and monitoring. That was useful as a long term vision, but it needed a narrower working draft that could actually be tested.

### What Was Learned

A strong Project 2 draft needs working components, not just a future product idea. The project needed to show a real workflow with tools, saved outputs, feedback, and monitoring logic.

## May 28, 2026

### Work Completed

1. Created the initial project environment.
2. Set up the Python virtual environment.
3. Installed dependencies.
4. Created the initial GitHub repository.
5. Created the basic project folder structure.
6. Started the first Streamlit app structure.
7. Added early source input fields.
8. Added the first version of public source intake.

### Why This Mattered

The project needed a working foundation before adding more advanced agentic features. The initial environment and Streamlit interface created the base for the rest of the build.

### What Was Learned

The app needed to be structured around a clear user flow. The most important early workflow was source intake, user role, report purpose, report generation, and output review.

## May 29, 2026

### Work Completed

1. Added OpenAI integration.
2. Added prompt files in the Prompts folder.
3. Added report generation logic.
4. Added report saving.
5. Added feedback logging.
6. Created Outputs and Tests folders.
7. Added selected report output sections.
8. Added role based customization.
9. Added early prompt workflow separation.

### Why This Mattered

This moved the app from a static interface into a working AI assisted application. It also started showing tool use because the app could generate a report, save the report, and save user feedback.

### What Was Learned

Prompt structure matters. The app needed separate prompt files and helper functions so the project did not become one large unstructured chat prompt.

## May 30, 2026

### Work Completed

1. Narrowed the project scope.
2. Defined the primary target audience as intelligence analysts.
3. Defined secondary audiences as emergency responders and the public.
4. Added stronger report sections, including Source Overview, Bottom Line Up Front, Executive Summary, So What or Why This Matters, Source Comparison and Reliability Notes, Confidence Assessment, Follow Up Questions, Requests for Information, and Forty Five Second Brief.
5. Updated the prompt structure so the report received the user role, report purpose, selected outputs, and custom instructions.
6. Continued aligning the app with the Project 2 agentic system requirement.

### Why This Mattered

The project needed a clear audience and a repeatable workflow. Narrowing the scope made the app easier to explain, easier to test, and easier to grade against the rubric.

### What Was Learned

TrendLens AI is strongest when it is described as a guided analysis workflow, not just an open text generator. The value is that the user does not need to know how to prompt the model correctly because the app structures the analysis process.

## May 31, 2026

### README Update

#### Work Completed

1. Rebuilt README.md.
2. Preserved the original project identity and core features.
3. Added the Project 2 working draft explanation.
4. Added the Weeks 3 to 4 agentic workflow requirement.
5. Added sections for reasoning, memory, tools, feedback, limited autonomy, model routing, and Model Context Protocol style design.
6. Added the semi automated monitoring concept.
7. Added the current development status and future improvements.

#### Why This Mattered

The README needed to show the professor that the project has a clear direction, working components, and an agentic system design. It also needed to avoid overclaiming features that were not fully implemented.

#### What Was Learned

The README should clearly separate working features from planned features. This makes the project more credible.

## May 31, 2026

### app.py Update

#### Work Completed

1. Rebuilt app.py around a three tab layout.
2. Added Generate Report, Monitoring Workflow, and About tabs.
3. Added target audience selection.
4. Added task type selection.
5. Added output depth selection.
6. Added report purpose input.
7. Added three public source input sections.
8. Added selected report sections.
9. Added optional custom instructions.
10. Added model route display.
11. Added an Agent Workflow Preview panel.
12. Added report generation.
13. Added report saving.
14. Added report download.
15. Added feedback logging.
16. Added safe optional monitoring imports.

#### Why This Mattered

The app interface now visibly demonstrates the agentic workflow. The user can see the steps the system follows, including source intake, validation, routing, report generation, saving outputs, feedback logging, and monitoring support.

#### What Was Learned

The agentic workflow needed to be visible in the app, not only described in the README.

## May 31, 2026

### monitoring.py Created

#### Work Completed

1. Created monitoring.py.
2. Added monitored topic saving.
3. Added monitored topic storage in the Monitoring folder.
4. Added previous source text and updated source text comparison.
5. Added similarity scoring.
6. Added added line and removed line detection.
7. Added keyword comparison.
8. Added possible significant update categories.
9. Added change summary output.
10. Added monitoring event logging.
11. Added last source text storage.
12. Added monitoring status summary.

#### Why This Mattered

This file made the semi automated monitoring concept real. Instead of only saying the app could monitor events, the project now has a tool that can compare old and new source text and identify meaningful changes.

#### What Was Learned

Monitoring should be described as semi automated in the working draft. The current version can compare changes and support scheduled checks, but full automated alerting would require an external scheduler, persistent storage, and possibly email notifications.

## May 31, 2026

### scheduler_worker.py Created

#### Work Completed

1. Created scheduler_worker.py.
2. Added a status command.
3. Added a scan once command.
4. Added due topic detection.
5. Added scheduler status output.
6. Added support for a five hour monitoring review cycle.
7. Added monitoring log updates.
8. Tested the scheduler status command.
9. Tested the scheduler scan once command.
10. Committed and pushed the scheduler worker.

#### Test Evidence

The scheduler status command returned zero topics, zero due topics, and a default five hour monitoring interval. The scan once command ran successfully and returned zero due topics because no monitoring topics had been saved yet.

#### Why This Mattered

This demonstrated the background worker concept for Project 2. It shows how the monitoring workflow could run on a timed cycle outside of the main Streamlit interface.

#### What Was Learned

Streamlit Community Cloud is useful for the app interface, but a true always running background scheduler should be deployed separately in a production version.

## May 31, 2026

### trend_tools.py Updated

#### Work Completed

1. Reviewed the original trend_tools.py file.
2. Preserved source cleaning.
3. Preserved URL text extraction.
4. Preserved prompt loading from the Prompts folder.
5. Preserved structured source block creation.
6. Preserved source consolidation.
7. Preserved selected output formatting.
8. Preserved report generation.
9. Preserved report saving.
10. Preserved feedback logging.
11. Added compatibility with the updated app.py.
12. Added model routing support.
13. Added metadata aware report saving.
14. Added fallback report behavior.
15. Added evaluation record helper support.

#### Why This Mattered

The first replacement version risked removing useful original features. The final merged version kept the original working tools and added the new Project 2 agentic workflow requirements.

#### What Was Learned

Code updates should preserve existing working features unless there is a clear reason to remove them. This was an important prompt design and code review moment.

## May 31, 2026

### Local Testing

#### Work Completed

1. Ran scheduler_worker.py with the status command.
2. Ran scheduler_worker.py with the scan once command.
3. Ran trend_tools.py from PowerShell.
4. Generated a sample TrendLens AI report about a chemical spill.
5. Confirmed the report included Source Overview, Bottom Line Up Front, Executive Summary, Source Comparison and Reliability Notes, Confidence Assessment, and Recommended Follow Up Questions.
6. Ran the Streamlit app locally with app.py.

#### Issue Encountered

The first trend_tools.py test appeared to hang during the OpenAI call and was stopped manually. Running the file again produced a complete report.

#### What Was Learned

The app should have fallback behavior and should not depend on a perfect model response every time. Testing also showed why saved outputs and evaluation files are important.

## May 31, 2026

### Streamlit Deployment

#### Work Completed

1. Connected the GitHub repository to Streamlit Community Cloud.
2. Deployed the app from the GitHub repository.
3. Troubleshot a blank page issue.
4. Identified that Streamlit was initially pointed at monitoring.py instead of app.py.
5. Corrected the deployed app so the main file path used app.py.
6. Confirmed the deployed app opened correctly.
7. Confirmed the app showed the Generate Report, Monitoring Workflow, and About tabs.

#### Issue Encountered

The deployed app initially appeared blank because Streamlit was running monitoring.py. That file is only a helper module and does not create the Streamlit user interface.

#### Resolution

The main file path was corrected to app.py.

#### What Was Learned

The deployed app must match the documentation. app.py is the interface file. monitoring.py, scheduler_worker.py, and trend_tools.py are helper files.

## May 31, 2026

### Deployed App Test

#### Work Completed

1. Opened the deployed TrendLens AI app.
2. Selected Intelligence Analyst as the user role.
3. Selected Create Executive Briefing as the task type.
4. Used Standard output depth.
5. Pasted a public weather article about Blue Moon viewing conditions in Metro Detroit.
6. Generated a full TrendLens AI report.
7. Confirmed the report included Source Overview, Bottom Line Up Front, Executive Summary, Five Ws, So What or Why This Matters, Source Comparison and Reliability Notes, Confidence Assessment, Follow Up Questions, and Forty Five Second Brief.

#### Why This Mattered

This test proved the deployed app could generate a real report from pasted public source text. It also showed the app could tailor the output for an intelligence analyst audience.

#### What Was Learned

The report output was stronger than expected. It showed that the structured workflow helps produce useful briefing style information even when only one source is provided.

## Prompt Design Notes

ChatGPT was used as a development partner during the build. The most useful AI support came from prompt design, project scoping, code review, troubleshooting, and documentation support.

Important AI assisted design decisions included:

1. Narrowing the project scope from a broad event monitoring platform to a focused public source situational awareness assistant.
2. Identifying the primary audience as intelligence analysts.
3. Identifying emergency responders and the public as secondary audiences.
4. Explaining how the app is more than a basic chatbot.
5. Adding visible agentic workflow steps to the app.
6. Creating separate tool files for reporting, monitoring, and scheduled checks.
7. Preserving useful original trend_tools.py functions instead of replacing them.
8. Correcting the gap between documentation and deployment when the deployed app initially pointed to monitoring.py instead of app.py.

## AI Pushback That Improved the Build

ChatGPT pushed back on several parts of the design. This helped make the project stronger.

1. The project should not claim full automation when the current version is semi automated.
2. The README should separate what is working from what is planned.
3. The app should not claim to independently verify public information.
4. The app should not use classified, private, restricted, or sensitive information.
5. The monitoring workflow should not be described as fully live alerting unless a separate background worker and notification system are implemented.
6. The deployed app should match the README claims.
7. The main Streamlit file must be app.py, not monitoring.py.

## Current Working Components

1. Streamlit interface.
2. Public source intake.
3. Target audience selection.
4. Task type selection.
5. Output depth selection.
6. Report purpose input.
7. Selectable report sections.
8. Model routing display.
9. Agent workflow preview.
10. Report generation.
11. Report saving.
12. Report download.
13. Feedback logging.
14. Monitoring workflow tab.
15. Manual old versus new source text comparison.
16. Monitoring topic saving.
17. Scheduler worker status command.
18. Scheduler worker scan once command.
19. GitHub repository.
20. Streamlit Community Cloud deployment.

## Known Limitations

1. Streamlit Community Cloud is used for the app interface, but it is not a full always running background worker.
2. Monitoring topics saved in file based storage may not be permanent in a hosted cloud environment.
3. Email alerts are not implemented yet.
4. User login is not implemented yet.
5. Long term user history would require a database.
6. Full automated monitoring would require a separate scheduler, cloud worker, or external automation service.
7. The app depends on the quality of the public source text provided by the user.
8. The app does not independently verify every fact.

## Next Steps

1. Update Tests/eval_results.md with real test results.
2. Add one saved report output to the Outputs folder.
3. Add screenshots for the deployed app and generated report.
4. Improve the Monitoring Workflow tab so users can choose check intervals in minutes or hours.
5. Add clearer old versus new source text display.
6. Add optional future email alert design.
7. Add database storage for persistent user history in a future version.
8. Continue improving prompt files for different audiences.
9. Commit and push the build log and evaluation results.
10. Submit the Streamlit app link and GitHub repository link for the Project 2 working draft.

## Final Reflection

The biggest progress this week was turning TrendLens AI into a working deployed app. The project now demonstrates a structured workflow, agentic design, tool use, model routing, monitoring support, and saved outputs. The most important improvement was making the project honest and testable. Instead of claiming full automation, the current build shows a realistic semi automated workflow with clear future expansion paths.