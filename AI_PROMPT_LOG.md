# TrendLens AI AI Prompt Log

## Purpose

This file documents how ChatGPT was used during the development of TrendLens AI. The goal is to show the prompt design process, major decisions, iterations, debugging steps, and lessons learned while building the Project 2 working draft.

TrendLens AI was developed as an agentic public event analysis and situational awareness reporting assistant. ChatGPT was used as a development partner to help narrow the scope, improve prompts, structure the workflow, troubleshoot code, deploy the app, and identify gaps between the documentation and the deployed application.

## How AI Was Used

ChatGPT was used for:

1. Project scope refinement
2. README development
3. Streamlit app structure
4. Prompt design
5. Agentic workflow planning
6. Model routing design
7. Monitoring workflow planning
8. Code review
9. Deployment troubleshooting
10. Evaluation planning
11. Build log documentation

The developer reviewed, tested, edited, committed, and deployed the final work.

## Key Prompting Workflow

The most useful workflow was asking ChatGPT to preserve existing working code before adding new features.

At one point, the updated trend_tools.py risked losing important original features such as source cleaning, URL extraction, prompt loading, structured source blocks, source consolidation, report saving, and feedback logging. The prompt was changed to specifically ask whether the original functionality was preserved. This helped identify that a merged version was safer than a full replacement.

This became an important project method:

1. Start with the current working file.
2. Ask AI what must be preserved.
3. Ask AI what new project requirements must be added.
4. Merge old and new functionality.
5. Test the file locally.
6. Commit only after the app still works.

## Prompt Design Iterations

## Iteration 1: Scope Refinement

Original direction:

TrendLens AI started as a broad situational awareness and event analysis platform for local, national, and international events.

Issue:

The idea was too broad for a working draft.

AI assisted change:

ChatGPT helped narrow the project into a public source analysis assistant that compares two or three public sources and generates a structured situational awareness report.

Result:

The project became easier to explain, test, and deploy.

## Iteration 2: Target Audience

Original direction:

The target audience included analysts, emergency management personnel, researchers, journalists, security professionals, students, and organizations.

Issue:

The audience was too broad.

AI assisted change:

The primary audience was narrowed to intelligence analysts. Emergency responders and the public were kept as secondary audiences.

Result:

The app now supports role based report generation and model routing.

## Iteration 3: Agentic Workflow

Original issue:

The app could have looked like a normal chatbot with a nicer interface.

AI assisted change:

ChatGPT helped define the visible agentic workflow:

1. Accept user role, purpose, task type, and public source text.
2. Validate source input.
3. Route the task to the correct model behavior.
4. Generate a structured report.
5. Save the report.
6. Save feedback.
7. Support monitoring checks for updated information.

Result:

The app now includes an Agent Workflow Preview panel that makes the agentic design visible to the user.

## Iteration 4: Monitoring Workflow

Original issue:

The README described monitoring, but the app needed real monitoring logic.

AI assisted change:

ChatGPT helped create monitoring.py and scheduler_worker.py.

Result:

monitoring.py compares previous source text against updated source text. It detects meaningful changes, added lines, removed lines, keywords, and possible significant update categories.

scheduler_worker.py supports timed review logic and a five hour monitoring cycle.

## Iteration 5: Deployment Debugging

Original issue:

The Streamlit app deployed as a blank page.

Cause:

Streamlit was pointed at monitoring.py instead of app.py.

AI assisted change:

ChatGPT helped identify that monitoring.py is only a helper file and app.py is the actual Streamlit interface.

Result:

The deployment was corrected to use app.py as the main file path.

## Important AI Pushback

ChatGPT pushed back on several claims that would have made the project less accurate.

Important corrections included:

1. Do not claim full automation when the current version is semi automated.
2. Do not claim the app independently verifies facts.
3. Do not use classified, private, restricted, or sensitive information.
4. Do not describe Streamlit Community Cloud as a true always running background worker.
5. Separate working features from planned future features.
6. Make sure the README matches the deployed app.
7. Keep monitoring.py as a helper file and app.py as the deployment file.

## Lesson Learned

The biggest lesson was that AI is most useful when it is asked to challenge the project, not just generate code.

The most helpful prompt pattern was:

"Preserve what already works, identify what is missing, and add the new feature without removing required functionality."

This helped prevent accidental loss of working features and made the project stronger.

## Final Reflection

ChatGPT helped turn TrendLens AI from a broad idea into a working deployed app. The strongest improvement was closing the gap between what the documentation claimed and what the deployed app actually showed. The final working draft now has a Streamlit interface, report generation, model routing, saved outputs, feedback logging, monitoring support, and scheduler worker logic.

The developer made the final decisions, tested the app, committed changes, pushed to GitHub, and deployed the app through Streamlit Community Cloud.
Britney:  no this was already done by a student for emails
no explicit build log documenting what you tried and changed (README and demo videos are a start, but document your iteration decisions); -1 pts: the tests folder needs actual eval output or pass/fail results committed to count fully — for P2, run your tests and commit the results.  -1pt: User interface/usability/value: Think about usefulness of the product and how the AI actually helps the user beyond generic advice, not just about building a product and your skills, but building it so that your beachhead user will extract immediate value out of it that would not be possible from a simple AI chat session after a braindump.  You have great ideas here, they just need to go a little further to show value not extractable from a chat agent.
what does he mean by this 
ChatGPT: He is basically saying three separate things:
He wants to see your development process, not just the final product.
Your Project 1 probably jumped from “idea” to “working app” without showing the middle steps. He wants evidence of iteration and decision making.
So instead of only having:
final code
README
demo video
He wants:
why you changed prompts
what failed
what improved outputs
why you chose one workflow over another
what problems you encountered
Example of what he wanted:
Commit 1:
 Basic prompt with unrestricted AI responses.
Problem:
 Responses were too broad and emotionally overwhelming.
Commit 2:
 Added phase-based logic.
Result:
 Responses became more structured but repetitive.
Commit 3:
 Limited output length and added stabilization-first prompting.
Result:
 Reduced cognitive overload and improved consistency.
That is the “build log documenting iteration decisions.”
Not just coding. Thinking.
Your tests folder needs actual proof the system was tested.
Right now you probably had a tests folder but no evidence of running tests.
He wants things like:
screenshots
terminal outputs
pass/fail logs
evaluation tables
before/after outputs
sample inputs and outputs
For example:
Test	Input	Expected	Actual	Result
 T1	User in crisis	Give stabilization advice only	Correct	PASS
 T2	User asks 10 things at once	Reduce overload	Partially repetitive	FAIL
 T3	User uploads document	Extract priorities	Correct	PASS
Then commit those results into GitHub.
He wants evidence the AI behavior was evaluated intentionally, not just “it worked on my screen.”
This is the biggest point:
 He thinks your app still feels too much like “just chatting with ChatGPT.”
This sentence is the key:
“show value not extractable from a chat agent”
Meaning:
 If someone can open regular ChatGPT and do basically the same thing with one prompt, then your app is not differentiated enough yet.
He is asking:
 “What does your system uniquely do that a normal AI chat does not?”
That is probably why your Project 1 lost usability/value points.
Your Tanglarity idea was good conceptually, but he likely wanted:
structured workflows
tracking
state retention
constrained decision logic
phase progression
visual organization
scoring
memory
guided actions
overload reduction mechanisms
specialized AI behavior
Instead of:
 “User types thoughts → AI gives advice.”
For Project 2, this matters a lot.
Your spam/scam idea becomes stronger if it does things normal ChatGPT does not easily do, such as:
tracking repeat caller patterns
assigning scam likelihood scores
detecting emotional manipulation tactics
categorizing scam types
summarizing voicemail risk
generating “safe response” recommendations
building a local spam history dashboard
showing why the AI flagged the call
identifying urgency/fear language patterns
That becomes an actual product workflow, not just “AI chat.”
Britney: ok let’s do a better job for project 2 with this do i copy my inputs for what im prompting here and what outputs i get?
ChatGPT: Yes — absolutely. That is exactly part of what he wants.
For Project 2, you should treat your prompting process almost like a mini research experiment and engineering journal.
You want to save:
prompts
prompt revisions
outputs
failed outputs
why you changed things
evaluation results
screenshots
test cases
commit history
Your professor is basically asking:
 “Can you prove intentional AI system design?”
Not just:
 “I made an app.”
A really strong setup for you would look like this:
Project Folder Structure
/project
 /app
 /prompts
 /tests
 /evals
 /docs
 README.md
Inside /prompts:
v1_prompt.txt
 v2_prompt.txt
 risk_scoring_prompt.txt
 emotion_detection_prompt.txt
Inside /evals:
evaluation_round1.csv
 evaluation_round2.csv
Example columns:
input_transcript
 expected_result
 actual_result
 risk_score
 notes
 pass_fail
Example:
“Final notice your loan application requires immediate verification…”
Expected:
 Spam/scam
Actual:
 High risk scam
Pass:
 YES
Then your build log can literally be:
docs/build_log.md
Example:
May 28:
 Initial model over flagged normal business calls as scams.
Change:
 Added urgency language weighting and whitelist logic.
Result:
 Reduced false positives from 6/10 to 2/10.
That is the kind of thing professors LOVE because it proves:
iteration
reasoning
evaluation
intentional engineering
The other huge thing:
 You need “product value beyond ChatGPT.”
So your app should NOT just be:
 “Paste voicemail → AI response.”
Instead build SYSTEM behavior.
For example:
Normal ChatGPT:
 “this sounds suspicious”
Your app:
extracts phone number
classifies scam category
highlights manipulation phrases
gives urgency score
tracks repeat patterns
stores call history
visualizes scam frequency
recommends next action
compares against previous calls
explains WHY it flagged it
THAT becomes a cybersecurity/consumer protection product.
That is the difference your professor is talking about.
Britney: ok i dont like this idea its been done by another student for the email spam or email phising detection im talking about
 nuisance calls about loans or other things that feel like a denial of service because of the amount being sent to my phone and legitimate calls, not coming through or having to silence my phone from all the spam calls. I might need a better problem to solve as well, but this seems to be a very common one. Are there currently things out there to help with this? 
Honestly, your instinct is correct. Email phishing detection is extremely overdone in student cybersecurity projects. Your professor will probably see “spam detection” and immediately compare it to generic classifiers unless you frame it differently.
But your actual problem statement is much stronger than “spam detection.”
The real problem you described is:
communication overload and disruption caused by nuisance call campaigns that interfere with legitimate communication
That is much more interesting.
Especially because:
phones are now operationally important
spam calls create alert fatigue
important calls get missed
users silence devices entirely
scammers exploit psychological interruption patterns
current tools are mostly reactive blocklists
That starts moving toward:
human factors
cognitive overload
operational disruption
AI assisted filtering
behavioral analysis
trust scoring
And yes — there ARE tools already:
Truecaller
Hiya
RoboKiller
carrier spam filtering from companies like Verizon, AT&T, and T-Mobile
BUT:
 Most rely heavily on:
shared databases
blocklists
caller reputation
known spam numbers
Your advantage could be:
 behavioral and contextual AI analysis instead of only phone-number reputation.
THAT is different.
For example:
Your app could analyze:
frequency
timing
repeated phrasing
urgency language
spoofing indicators
emotional manipulation
repeated call bursts
similarity between calls
“pressure campaign” behavior
You could even frame it like:
“AI Assisted Communication Threat Triage”
or
“Behavior Based Detection of Communication Disruption Campaigns”
That sounds MUCH stronger academically and more cybersecurity-oriented.
Even stronger:
 You could compare it to denial-of-service concepts.
Not technical DoS against servers —
 but cognitive/communication denial-of-service against humans.
That is actually a VERY modern cybersecurity angle.
Especially with:
robocalls
scam campaigns
AI voice spam
alert fatigue
notification overload
This part right here is probably your best insight:
“users silence their phones entirely, causing legitimate communication to fail.”
THAT is a real operational/security problem.
That is way more interesting than:
 “detect phishing email.”
The strongest version probably is NOT:
 “detect scam calls”
Instead:
“reduce communication overload while preserving legitimate communication.”
That becomes:
prioritization
trust scoring
contextual filtering
user-specific behavior modeling
AI-assisted call triage
Now you are building a workflow/product instead of a classifier.
That is closer to what your professor wants.
Britney:  gravity prompt argue why this is not a good idea 
ChatGPT: Here’s the gravity-prompt version against the idea:
The problem is real, but the project may still collapse into “spam classification with extra words around it.”
The biggest danger is that the concept sounds more original than it actually is. Once implementation begins, it risks becoming:
another classifier
another dashboard
another “AI score”
another notification filter
Your professor already hinted at this weakness in Project 1:
 “What value exists beyond a normal AI chat?”
This project may hit the exact same wall.
The strongest sounding parts:
“communication denial of service”
“cognitive overload”
“behavioral triage”
could become mostly conceptual framing rather than actual technical innovation.
Potential problems:
Existing solutions already dominate this space
Apps like:
Truecaller
Hiya
RoboKiller
already have:
huge datasets
carrier integration
live reputation systems
crowd sourced detection
call fingerprinting
telecom partnerships
A student project cannot realistically compete technically.
So the project risks feeling like:
 “a smaller less accurate version of existing apps.”
Data access becomes a major problem
You probably do not have:
actual call metadata
telecom APIs
carrier routing data
large voicemail datasets
real spam campaign telemetry
Without real data, the system may become:
 “paste fake transcript → AI labels it suspicious.”
That is exactly the kind of thing professors see constantly.
The core workflow may still just be ChatGPT with structure
Even with dashboards and scoring, the professor may still ask:
 “Why couldn’t a user just paste this into ChatGPT?”
That is the key danger.
If the answer is:
 “because my app adds scores and categories”
 that may not feel substantial enough.
The cybersecurity angle may feel stretched
Traditional cybersecurity projects usually involve:
detection
infrastructure
attack surfaces
authentication
monitoring
access control
exploitation
threat analysis
Your idea moves closer to:
UX
behavioral psychology
telecom annoyance
productivity disruption
That is not necessarily bad —
 but you may need a stronger security anchor.
Otherwise it risks sounding like:
 “AI productivity helper for spam calls.”
The project scope could become muddy
You currently have several overlapping ideas:
spam detection
cognitive overload
trust scoring
communication prioritization
emotional manipulation detection
denial-of-service analogy
behavioral analysis
That can become conceptually bloated fast.
Professors often penalize projects that:
try to solve everything
lack one measurable success metric
have vague system goals
You may be choosing the problem because it emotionally resonates, not because it is technically strong
That matters.
A project being personally frustrating does not automatically make it academically valuable.
You still need:
measurable outputs
defensible architecture
testability
evaluation metrics
a clear “AI advantage”
Without those, the project may feel more like a complaint translated into software.
The strongest criticism:
 The project currently sounds stronger philosophically than technically.
That does not mean abandon it.
 It means:
 the implementation path still needs a concrete differentiator that is technically defensible, testable, and hard to replicate with a simple prompt.

Britney: ok lets go a different direction then some problems that could be solved let’s brainstorm:
 - maybe a problem with the post office and change of address not actually getting adapted even when doing so and paying for a P.O. box
 - gap in military not having assistance specifically for domestic violence and them always removing the victim not the perpetrator but this is emotional not something for an app
 - cybersecurity large data centers employing anyone and having misfires from workers desk pops, and needing to train better and have a better hiring pool
 - an app for what else are some ideas for cybersecurity that are gaps or problems currently that need to be addressed 

ChatGPT: You are actually circling around a MUCH better category now:
 human centered cybersecurity and operational failure gaps.
Those are harder to copy from generic tutorials and usually create stronger projects because they connect:
real workflows
human behavior
operational risk
AI assisted decision making
Here are the strongest ideas from your direction, with gravity analysis built in:
AI Assisted Security Incident Prioritization for Overwhelmed Analysts
Problem:
 SOC analysts get flooded with alerts and start ignoring or misprioritizing events.
Real issue:
 Alert fatigue is a massive cybersecurity problem.
Your app:
ingests mock alerts/logs
groups similar alerts
prioritizes likely real threats
explains why
reduces duplicate noise
creates an analyst workflow summary
Why this is strong:
real cybersecurity problem
measurable
easy to simulate
lots of AI opportunity
beyond generic chatbot
can visually demonstrate value
Why professors like it:
 Feels operational and enterprise relevant.
Insider Risk Behavioral Drift Detection
Problem:
 Employees often show behavioral warning signs before security incidents.
Your app:
analyzes simulated employee behaviors
detects unusual access/activity patterns
flags risk escalation
explains contributing factors
Could include:
unusual login times
USB activity
abnormal downloads
policy violations
emotional/frustration indicators in tickets or messages
Why strong:
 Very modern cybersecurity topic.
Why dangerous:
 Can become ethically messy or feel dystopian if framed poorly.
AI Assisted Cybersecurity Training Gap Analyzer
THIS actually connects well to your “bad hiring/training pool” thought.
Problem:
 Cybersecurity teams hire people with certifications but weak operational judgment.
Your app:
presents mini scenarios
evaluates responses
identifies knowledge gaps
adapts future training
measures decision quality instead of memorization
This is actually VERY strong because:
measurable
interactive
easy to build
AI adds real value
strong workflow differentiation
Could simulate:
phishing
incident escalation
privilege misuse
physical security
social engineering
This may honestly be one of your best options.
AI Assisted Policy Translator
Huge real problem.
Problem:
 Security policies are unreadable to normal employees.
Your app:
converts technical policy into plain language
creates role specific summaries
generates “what this means for me”
quizzes comprehension
Example:
 Original:
 “Multi factor authentication shall be enforced…”
Output:
 “As an employee, this means…”
Why strong:
huge organizational gap
realistic
AI useful
easy to demonstrate
highly testable
Misconfiguration Risk Scanner for Small Businesses
Problem:
 Small businesses misconfigure cloud/storage constantly.
Your app:
scans mock configs
explains risks
prioritizes fixes
generates plain language remediation
Could simulate:
open S3 buckets
weak IAM
exposed ports
MFA disabled
bad password policies
Very practical.
 Very cybersecurity.
 Very demonstrable.
AI Assisted Digital Forensics Triage
This aligns with your CIS 617 background.
Problem:
 Investigators waste time manually sorting artifacts.
Your app:
ingests logs/files
categorizes suspicious artifacts
creates investigation timelines
prioritizes evidence
Could use:
fake PCAPs
Windows event logs
browser history
suspicious processes
This would look VERY technical on a portfolio.
“Desk Pop” / Human Error Risk Simulator
This one is unique.
Problem:
 Human operational mistakes inside sensitive environments create security incidents.
Your app:
simulates employee decision making
predicts likely failure points
identifies training weaknesses
generates intervention recommendations
Could apply to:
data centers
military
SOCs
hospitals
aviation
This becomes:
 human reliability engineering + cybersecurity.
Very unique if done well.
AI Assisted Resource Navigation for Complex Systems
This one is subtle but potentially excellent.
Problem:
 Organizations have resources, but users cannot navigate them effectively.
Could apply to:
military
VA
universities
cybersecurity incident reporting
housing support
internal HR systems
The AI:
asks clarifying questions
maps workflows
identifies gaps/dead ends
generates next-step plans
Why this could work:
 It is operational systems analysis, not therapy.
This is actually closer to your Tanglarity strengths but framed more professionally.
My strongest recommendations for YOU specifically:
Best balance of:
originality
feasibility
technical depth
portfolio value
professor appeal
Top 3:
AI Assisted Security Alert Prioritization
Cybersecurity Training Gap Analyzer
Digital Forensics Triage Assistant
Those three:
clearly use AI
solve real operational problems
are testable
avoid “just another chatbot”
fit your cybersecurity background
allow structured workflows
naturally produce evaluation metrics and logs
And most importantly:
 they are easier to prove value beyond normal ChatGPT.
Britney: give me a list of more problems in cybersecurity currently to solve like the gap with the human error like my capstone project and all
ChatGPT: Here are stronger “real gap” cybersecurity problems that are happening right now, especially around human behavior, operations, workflow failures, and overload rather than just technical exploits.
These are the kinds of problems professors and employers usually find more interesting because they are harder to solve than “detect malware.”
Alert fatigue in Security Operations Centers (SOCs)
 Analysts ignore real threats because they receive thousands of repetitive alerts daily.
Misconfigured cloud storage and permissions
 Companies accidentally expose sensitive data because IAM roles, S3 buckets, or access permissions are confusing.
Poor cybersecurity communication between technical and nontechnical teams
 Executives and employees do not understand risk severity because reports are too technical.
Overreliance on certifications instead of operational competency
 Organizations hire people with certifications but weak real world decision making skills.
Human error during incident response
 Employees accidentally worsen breaches by shutting down systems incorrectly, deleting evidence, or escalating improperly.
Shadow IT and unauthorized applications
 Employees use unapproved apps and cloud services because official workflows are too slow or difficult.
Password fatigue and unsafe credential behavior
 Users reuse passwords or bypass MFA because security controls become frustrating.
Insider threat detection gaps
 Organizations struggle distinguishing malicious insider activity from stressed, overwhelmed, or careless employees.
Poor vulnerability prioritization
 Security teams patch low risk systems while critical vulnerabilities remain exposed.
AI generated phishing and social engineering
 Attackers now generate convincing personalized phishing at scale using AI.
Burnout in cybersecurity teams
 Constant high pressure environments reduce analyst performance and increase mistakes.
Inadequate security awareness training
 Most training is generic compliance material that employees ignore immediately after completion.
Poor handoff between shifts in SOCs or operational teams
 Critical threat context gets lost between personnel changes.
Insecure remote work environments
 Employees mix personal and work devices/networks with weak controls.
Excessive permissions and privilege creep
 Employees accumulate access over time that never gets removed.
Security policy overload
 Policies become so long and unreadable that nobody follows them.
Deepfake voice and impersonation scams
 Organizations increasingly cannot verify if calls or voice messages are authentic.
Third party vendor trust problems
 Organizations depend on vendors with weak security practices they cannot fully monitor.
Security tool overload
 Companies buy too many security platforms that do not integrate well, overwhelming analysts.
Inadequate logging and telemetry retention
 Organizations discover after a breach that the evidence they needed was never collected.
AI hallucinations in cybersecurity workflows
 Analysts may trust AI generated explanations that are partially incorrect.
Poor phishing reporting workflows
 Employees often do not report suspicious emails because the process is annoying or unclear.
Data center physical security complacency
 Tailgating, badge misuse, and unsafe physical behaviors happen because employees normalize shortcuts.
Lack of contextual training for military or high stress environments
 Training often does not simulate realistic stress, fatigue, or operational pressure.
Miscommunication during cyber incidents
 Technical teams, management, legal, and public affairs often interpret situations differently during breaches.
Weak onboarding/offboarding processes
 Former employees sometimes retain access long after departure.
Cognitive overload in cybersecurity analysts
 Analysts struggle processing large volumes of logs, dashboards, alerts, and tickets simultaneously.
False positive overload in threat detection systems
 Security tools create so much noise that teams become desensitized.
Poor cybersecurity resource navigation
 Employees cannot figure out who to contact, what policy applies, or what tool to use during incidents.
Unsafe AI adoption inside organizations
 Employees paste sensitive company information into public AI tools without understanding the risks.
Inconsistent risk scoring across teams
 Different departments interpret “critical” risk differently, causing prioritization failures.
Security theater instead of actual security
 Organizations focus on visible compliance actions rather than meaningful risk reduction.
Incident documentation gaps
 Teams fail to properly document lessons learned after security events.
Human trust exploitation
 Attackers increasingly manipulate urgency, authority, loneliness, or emotional stress rather than exploiting software.
Cybersecurity staffing shortages causing operational shortcuts
 Organizations skip proper review processes because teams are understaffed.
Poor operational visibility across hybrid environments
 Teams struggle monitoring cloud, on premises, and remote systems together.
Overconfidence in automation
 Organizations trust automated systems too heavily without human verification.
Failure to adapt training to employee roles
 Everyone receives the same training regardless of their actual risk exposure.
Weak escalation criteria
 Employees are unsure what constitutes “serious enough” activity to report.
Gaps between policy and reality
 Organizations create idealized security procedures that do not match how employees actually work.
The strongest projects usually:
focus on ONE operational pain point
have measurable outcomes
involve workflow improvement
demonstrate AI assisted decision making
include human factors
show before/after improvement
are testable with scenarios or simulations
Your capstone style thinking around human error, operational failure, overload, and system gaps is actually a strong direction because it is much harder to copy from generic GitHub projects.
Britney:  rate by what i could have the most impact on and what is most commonly seen as a problem 
ChatGPT: Here’s how I would realistically rank them based on:
real world impact
how widespread the problem is
how much organizations actually struggle with it
how strong it could be as a project
how feasible it is for one student
whether AI genuinely adds value
whether it avoids “generic chatbot syndrome”
Top Tier — strongest combination of impact + feasibility + originality
Alert Fatigue / Security Alert Prioritization
 Impact: Extremely high
 Commonness: Everywhere
 Project strength: Excellent
Why:
 This is one of the biggest modern cybersecurity problems. SOC teams drown in alerts and miss real threats because of overload.
AI value:
 Very strong.
 AI can:
group alerts
reduce duplicates
summarize incidents
prioritize severity
explain reasoning
Why this is probably your best overall option:
measurable
realistic
operational
cybersecurity aligned
easy to simulate
hard to dismiss as “just ChatGPT”
You could literally show:
 Before AI:
 300 alerts
After AI:
 12 grouped incidents prioritized by risk.
That is tangible value.
Cybersecurity Training Gap Analyzer
 Impact: Extremely high
 Commonness: Everywhere
 Project strength: Excellent
Why:
 Most cybersecurity training is terrible and does not measure operational judgment.
This connects directly to:
human error
weak hiring pools
operational mistakes
desk pops
unsafe decisions
AI value:
 Adaptive evaluation.
 Scenario analysis.
 Decision scoring.
Why strong:
 You can demonstrate:
user improvement
gap detection
customized training
Very portfolio friendly.
Human Error / Operational Risk Prediction
 Impact: Extremely high
 Commonness: Extremely common
 Project strength: Very strong if scoped correctly
This is closest to your capstone mindset.
Problem:
 Organizations spend millions on tools while ignoring operational human failures.
Examples:
wrong config pushed
accidental exposure
poor escalation
unsafe shortcuts
rushed actions
AI value:
 Pattern recognition.
 Scenario simulation.
 Risk scoring.
Danger:
 Can become vague philosophically unless grounded in measurable workflows.
Still very strong.
Second Tier — very impactful but harder to execute well
AI Assisted Digital Forensics Triage
 Impact: High
 Commonness: High
 Project strength: Very technical
Strong because:
aligns with your experience
very demonstrable
feels advanced
Weakness:
 Requires more technical setup and data handling.
Misconfiguration Risk Scanner
 Impact: Very high
 Commonness: Extremely common
 Project strength: Strong but common
Very practical.
 But:
 lots of existing tools already exist.
You would need a unique angle:
 “plain language remediation”
 or
 “AI assisted prioritization.”
Security Policy Translator
 Impact: High
 Commonness: Extremely common
 Project strength: Strong but less “cyber cool”
Actually a massive problem.
 But professors sometimes undervalue communication projects unless framed carefully.
Could become:
 “role aware policy comprehension engine.”
Third Tier — interesting but riskier academically
Insider Threat Behavioral Drift
 Impact: Very high
 Commonness: Common
 Project strength: Dangerous territory
Why risky:
ethics concerns
privacy concerns
difficult to model realistically
easy to sound dystopian
Resource Navigation / Complex Systems Guidance
 Impact: High
 Commonness: Extremely common
 Project strength: Hard to frame technically
This is actually valuable in reality.
 But professors may see it as:
 “AI assistant chatbot.”
Unless the workflow differentiation is VERY strong.
Lower Tier — weaker for a cybersecurity project
Scam Call Prioritization
 Real problem:
 Yes.
Academic differentiation:
 Harder.
Risk:
 Feels too close to existing spam filtering systems.
Post Office / Change of Address Problems
 Real problem:
 Yes.
Cybersecurity relevance:
 Weak unless reframed around identity verification or fraud prevention.
My recommendation for YOU specifically:
Best balance:
Alert fatigue / AI SOC prioritization
Cybersecurity training gap analyzer
Human operational risk / human error reduction
Why these fit YOU:
you think operationally
you think in workflows
you naturally identify human/system disconnects
you already analyze failures in processes
you have military + cybersecurity perspective
you can explain human factors well
Your biggest strength is not:
 “coding a classifier.”
Your strength is:
 understanding where systems fail operationally because humans, workflows, overload, and reality do not match the design assumptions.
That is actually a valuable cybersecurity perspective.

Britney:  what is currently out there for this already gravity prompt this idea 
Chatgpt: If you choose the “AI assisted alert fatigue / SOC prioritization” idea, here’s the gravity prompt against it:
This is already an active industry battlefield.
Major companies are pouring billions into solving this exact problem:
CrowdStrike
Palo Alto Networks Cortex XSIAM
Microsoft Sentinel
Splunk SOAR
Google SecOps
Modern SOC platforms already:
prioritize alerts
correlate events
suppress duplicates
enrich incidents
automate triage
generate summaries
reduce false positives
use AI agents
automate investigations
The entire industry knows alert fatigue is a massive problem.  
So the danger is:
 your project becomes “small student version of enterprise SIEM/SOAR tooling.”
That is hard to differentiate.
Another danger:
 you probably will not have:
real enterprise telemetry
production SOC data
actual analyst workflows
live integrations
high volume environments
Without realistic data, the project can become:
 “fake alerts into fake dashboard.”
Professors notice this quickly.
Another major issue:
 many AI SOC tools are already marketing exactly the same language:
“reduce alert fatigue”
“prioritize threats”
“AI assisted triage”
“human AI teaming”
“autonomous SOC”
Even academic research is already heavily focused on this exact space.  
Meaning:
 your project risks sounding trendy rather than original.
Another important weakness:
 the scope can explode.
Once you start:
ingestion
correlation
severity scoring
enrichment
automation
timelines
workflows
analyst summaries
recommendations
you accidentally start rebuilding a SIEM/SOAR ecosystem.
That is not realistically achievable for one semester.
Most dangerous issue:
 AI hallucinations in cybersecurity are extremely risky.
If your AI:
suppresses a real threat
misprioritizes an incident
gives incorrect analysis
then the whole value proposition becomes questionable.
Enterprise companies solve this with:
huge training datasets
threat intel feeds
rule engines
analysts
orchestration systems
human validation
mature pipelines
A student project likely cannot reliably reproduce that.
The strongest criticism:
 The problem is absolutely real, but the market is already saturated with companies and research trying to solve it.
So your project would need a VERY narrow niche or differentiator.
For example:
 BAD version:
 “AI SOC alert prioritization”
BETTER version:
 “AI assisted prioritization for junior analysts using explainable reasoning and training feedback.”
Or:
 “Reducing alert fatigue for small organizations without enterprise SOC tooling.”
Or:
 “Human-AI collaboration workflows instead of autonomous triage.”
That narrows the scope and gives you a defendable angle instead of competing against billion dollar SIEM vendors.


my input: yes ok what can i have the most impact over that does not fall into a student version of something already known and solving the gaps? i need to come up with an original idea like in the military there is a lot of new systems always being implemented and not all soldiers have an army email due to funding, our systems act like its going through a DOS attack with how slow and how many times it kicks you out of websites you need for your job or microsoft licensing issues which is a big funding issue, also these a large problems that would have been solved already if possible. military problems dont encompass a large population too its too specific not many common users then. we could do something for teaching better public speaking with structured repetition and analytical methods a lot of people struggle with public speaking but there is a formula for it those who are good do it naturally or have those conversations in their personal lives….also how do people keep up with the news or the world current and future issues. Drones and UAS and Cyber attacks but my student app couldnt possibly in two weeks solve anything with that is there another angle or something I have not considered yet? look back into my search is there a gap in peoples compassion or fantasy versus reality or ideal self and real self

Project 2 Ideation Transcript and Iteration Notes
Initial Project Direction:
 The original concept focused on nuisance robocalls, spam loan calls, and communication overload. The concern was not simply spam detection, but the operational disruption caused by constant nuisance calls forcing users to silence phones and potentially miss legitimate communication.
Reflection and Problem Reassessment:
 During brainstorming, concerns emerged that this idea was too close to existing spam and phishing detection systems already developed by both industry and previous students. Existing products such as Truecaller, carrier spam protection, and enterprise filtering systems already dominate this space with massive datasets and infrastructure unavailable to a short term student project.
A deeper issue was identified:
 The concept risked becoming “another classifier” or “another AI chatbot with scores,” rather than demonstrating unique workflow value beyond what could already be achieved through a standard AI chat interface.
Expanded Operational Observations:
 Additional operational and cybersecurity related gaps were considered, including:
Military systems experiencing severe slowness, login failures, and repeated timeout behavior similar to denial of service conditions
Frequent Microsoft licensing and access issues preventing operational efficiency
Uneven adoption of Army email systems due to funding constraints
Human error inside cybersecurity and operational environments
Poor communication and public speaking confidence despite technically capable personnel
Gaps between intended behavior and actual behavior in leadership, communication, and operations
Cognitive overload and difficulty keeping up with world events, cybersecurity developments, and emerging threats
Key Insight Identified:
 The strongest recurring pattern across discussions was not purely technical cybersecurity, but operational human performance gaps:
Systems assume humans operate consistently under stress
Real world communication often breaks down under pressure
Operational confidence is usually developed through repeated structured exposure
Many people lack frameworks for clear communication, leadership speaking, or analytical conversational structure
Potential New Project Direction:
 The revised concept shifted toward an AI Assisted Communication and Decision Calibration System.
Core Focus:
 A structured AI assisted workflow that helps users improve:
Public speaking
Leadership communication
Difficult conversations
Briefing structure
Confidence under pressure
Analytical response formulation
Potential Features:
Scenario based conversational simulations
Structured repetition and adaptive practice
BLUF style response generation
Detection of filler words and uncertainty patterns
Comparison between intended message and actual delivery
Progress tracking and confidence scoring
Analytical feedback on clarity, organization, and operational communication
Reason for Direction Change:
 This direction better addresses:
Human operational friction
Communication breakdowns
Real world workflow gaps
Measurable behavioral improvement
This concept also avoids becoming:
another generic chatbot
another spam classifier
another enterprise cybersecurity clone project
Most Important Lesson from Iteration:
 The strongest project ideas may not come from attempting to “solve cybersecurity” directly, but from improving the human operational bottlenecks that repeatedly cause system failures, communication failures, and poor decision making inside cybersecurity and leadership environments.
You are actually getting closer now because you are finally thinking about:
 “What problem exists because systems assume humans function perfectly?”
THAT is where the real gaps are.
And honestly, your strongest ideas are not “technical cybersecurity tools.”
Your strongest ideas are:
 human operational failure systems.
That is much more original.
You are also correctly identifying something important:
 If billion dollar organizations have not solved something already, a two week student project will not “solve” it either.
So your goal should NOT be:
 “solve cybersecurity.”
Your goal should be:
 build a focused AI assisted workflow that improves one measurable human bottleneck.
That is realistic.
Looking at YOUR patterns specifically:
operational thinking
military workflows
human error analysis
emotional vs procedural disconnects
overload
communication
training gaps
systems that do not match reality
ideal self vs actual behavior
structured thinking under pressure
You are naturally identifying:
 cognitive friction problems.
That is your niche.
And honestly?
 That is probably more original than another technical cyber tool.
The strongest idea I think you are circling is NOT:
 “cybersecurity AI.”
It is:
AI Assisted Human Performance Calibration
Or simpler:
“Gap between intended behavior and actual behavior.”
That is HUGE across:
military
cybersecurity
leadership
communication
relationships
training
public speaking
incident response
decision making
And very few student projects approach this well.
Your public speaking thought is actually stronger than you realize.
Not:
 “AI speech coach.”
That is already done.
BUT:
 “AI structured conversational repetition and operational confidence trainer”
THAT is different.
Because your insight is:
 people who appear naturally articulate usually have:
repeated exposure
conversational pattern memory
structured framing
topic familiarity
emotional regulation under pressure
Your app could:
simulate difficult conversations
identify weak response patterns
detect filler words
detect uncertainty patterns
train structured responses
reinforce repetition
build adaptive questioning
teach conversational frameworks
compare intended message vs actual delivery
This connects directly to:
military leadership
interviews
cybersecurity briefings
executive communication
operational confidence
analyst presentations
emotional regulation under pressure
THAT is actually extremely valuable.
And importantly:
 it is not easily replaced by plain ChatGPT.
Because the workflow matters.
The system becomes:
iterative
analytical
comparative
progress tracking
adaptive
scenario based
Now you are building:
 a training system.
NOT:
 a chatbot.
Another VERY strong angle:
AI Assisted Reality Gap Analyzer
This is honestly one of the most original concepts you mentioned.
Problem:
 People often confuse:
ideal self
intended behavior
fantasy
stated values
actual patterns
operational reality
This applies everywhere:
cybersecurity
leadership
relationships
military readiness
organizational policy
hiring
training
public communication
Example:
 Organization says:
 “security is our priority.”
Reality:
passwords reused
MFA bypassed
alerts ignored
shortcuts normalized
OR:
Person says:
 “I communicate clearly.”
Reality:
fragmented speech
indirect requests
emotional escalation
avoidance patterns
An app that:
 compares intended behavior vs actual behavior patterns
is honestly VERY sophisticated conceptually.
BUT:
 dangerously hard to scope in two weeks.
So I would NOT do the full philosophical version.
Instead:
 narrow it to ONE measurable area.
My honest recommendation for YOU specifically:
Best project fit:
 AI Assisted Communication and Decision Calibration System
Focused on:
public speaking
leadership communication
operational briefings
interviews
difficult conversations
structured response building
Why this works:
measurable
testable
highly human
AI genuinely useful
unique angle
realistic in 2 weeks
ties into military/cybersecurity
avoids generic “AI assistant”
avoids impossible enterprise problems
workflow based
adaptive
strong portfolio value
You could literally demonstrate:
 Before:
 fragmented answer under pressure.
After:
 structured BLUF response with confidence scoring.
THAT is tangible.
And it aligns with something you already naturally analyze:
 why some people communicate effectively under pressure while others collapse cognitively or emotionally.
That is actually a very important operational problem.
5/28/2026
 Britney: ok my project 2 for . These systems leverage four core pillars: Reasoning (planning), Memory (context), Tools (APIs/actions), and Feedback (refinement) cannot be the same as any of these it must be original and what about when Analysts get spreadsheets of raw data and need to organize it into something that can be reported like for me right now I have a spreadsheet of my military units security clearance issues and I need to break it down into these categories by 8 different units and they want to know those that have expired, expiring in 30 days, expiring in 60-90 days, no determination made, action required, or pending G2 action. The problem is this is on a Army Remote desktop and I not accessible to the public plus the information is classified so is there an equivalent to something like this but for analysts on the civilian side? What other ideas would be best? I was also thinking about how I need to create meaningful training at my unit level but don't have the support how do we transform and be able to create meaningful tailored training to ourselves and soldiers that we can train on in our off time that is not classified? What about how the S2 has to track the international, national, and local news but there is so much going on in the world how do we keep up and find patterns or identify what is normal or outside the norm or do any pattern analysis in events occuring around the world Significant activity tracker SIGACT? This could be specific to those having to inform others on the news but also the broader population who needs to know what is going on and gain valuable insight from it as well as pull from local news because things are always updating and have the agent give a few products something like a raw tracker, a digestible view of trends with what patterns are being tracked, then a high table top overview to brief to someone like an elevator pitch in 45 sec 

ChatGPT: Yes. The strongest idea is the civilian version of your S2 tracker.
Best Project 2 concept:
SIGACT Sense AI
An agentic public event tracker that turns messy local, national, and international news into structured reporting products.
Problem statement:
People who need to stay informed, such as analysts, emergency managers, students, journalists, security teams, or community leaders, are overwhelmed by fast moving local, national, and international events. News is scattered across sources, changes quickly, and is difficult to organize into patterns, trends, and briefable summaries. A normal AI chat can summarize one article, but it does not automatically structure events, categorize significance, compare patterns over time, or produce multiple reporting products for different audiences.
Your app could take public news links, article text, or manual event entries and output:
Raw tracker
Date, location, source, category, event type, scope, actor, impact, confidence, and follow up questions.
Analyst trend view
What patterns are emerging, what is increasing, what seems unusual, and what should be monitored.
45 second brief
A short commander or executive style summary.
RFI list
What information is missing and what should be checked next.
This fits the four pillars perfectly:
Reasoning:
The app decides what type of event it is, whether it is local, national, or international, and what product should be generated.
Memory:
It stores past events so the system can compare new activity against previous activity.
Tools:
It can use news URLs, uploaded spreadsheets, article text, categorization tools, trend scoring, and export tools.
Feedback:
The user can correct the category, significance, or analyst comment, and the system can refine future outputs.
This is better than using your actual military clearance spreadsheet because it avoids classified or sensitive information. It also has a civilian audience: emergency management, corporate security, local government, journalists, nonprofit leaders, students, or anyone who needs to track public events.
Your spreadsheet already supports this idea because it has event tracker fields like command, scope, location, links, analyst comment, and references. The public version can keep that same workflow without using military sensitive data.
The best project options ranked:
SIGACT Sense AI
Public news and significant activity tracker. Best overall. Most original, strongest agentic fit, and directly connected to your real analyst workflow.
Civilian Data Triage Agent
Uploads messy spreadsheets and categorizes rows into reportable groups. Good, but less unique unless you give it a specific use case like nonprofit case tracking, emergency incidents, or compliance issues.
Training Builder Agent
Creates tailored training from role, skill gaps, time available, and scenario needs. Useful, but may look more like content generation unless you add assessments, feedback loops, and progression tracking.
Scam Call Analyzer
Useful and relatable, but another classmate already has a phishing detector, so this may overlap too much.
I would pick SIGACT Sense AI. It is original, useful, civilian safe, and naturally shows agentic behavior.
ok it needs to be public I keep the add readme toggled off because I am making one right or do i toggle it on? do I click no.gitingnore what do I select from the dropdown? and for license what do I click
Yes — exactly.
Use these settings:
Repository:
Public ✅
README:
Leave UNCHECKED ❌
 Because you already created your own local README.md
.gitignore:
Select:
None
Because you already created your own .gitignore locally.
License:
Select:
None
You can always add a license later if needed.
This avoids merge conflicts and keeps your local project as the “source of truth.”
ok now what how do I link them?
After you click “Create Repository,” GitHub will show a page with commands.
You want the section that says something like:
…or push an existing repository from the command line
Copy the TWO commands that look like this:
git remote add origin https://github.com/YOURNAME/trendlens-ai.git
and
git push -u origin master
Then:
Paste the FIRST command into your VS Code terminal
 Press Enter
Paste the SECOND command
 Press Enter
GitHub may open a login/authentication popup.
 Approve it if it appears.
Then refresh GitHub and your files should appear online.
VERY IMPORTANT:
 Before pushing, double check again:
 your .env file is NOT showing in VS Code Source Control changes.
You already did this correctly earlier, but it is worth one last quick check.
Thought for 6s
Next build the prompt files.
Go to:
Prompts/system_prompt.md
Paste this:
You are TrendLens AI, an agentic situational awareness and public event analysis assistant.

Your purpose is to help users transform public information sources into structured analyst style reporting products. The user may provide article text, event descriptions, public alerts, press releases, or source notes. Your task is to compare the sources, identify what matters, and create a clear situational awareness product.

Core behavior:

1. Use only the information provided by the user.
2. Do not invent facts, dates, locations, actors, motives, or outcomes.
3. Clearly state when information is missing, unclear, or not provided.
4. Separate confirmed information from possible implications.
5. Focus on patterns, significance, uncertainty, and follow up needs.
6. Write in a clear analyst style that is useful for briefing.
7. Avoid emotional language or exaggerated claims.
8. Avoid making legal, medical, or official emergency recommendations.
9. Use concise professional language.
10. Prioritize practical value over generic summarization.

Agentic workflow expectations:

Reasoning:
Evaluate the source material, identify the main issue, determine significance, compare themes, and explain why the information matters.

Memory:
Consider the current report context and preserve important details during the session when available.

Tools:
Use structured analysis steps, source extraction, categorization, risk framing, confidence assessment, and briefing generation.

Feedback:
Treat user feedback as guidance for improving clarity, usefulness, and specificity in later outputs.

Output expectations:

Always produce structured reporting. Do not respond as a casual chatbot. The final report should help the user quickly understand the situation, key patterns, risks or concerns, and next questions to research.
Then create a second file:
Prompts/report_prompt.md
Paste this:
TrendLens AI Report Format

1. Source Overview

For each source, identify:
Date of article if available
Date of event if available
Location if available
Main topic
Relevance to the overall situation

2. Bottom Line Up Front

Provide 1 to 3 sentences explaining what matters most.

3. Executive Summary

Provide a concise paragraph explaining the overall situation.

4. So What

Explain why this matters and who may care.

5. Key Trends

Identify patterns, repeated themes, escalation indicators, changes over time, or notable gaps across the sources.

6. Risks or Concerns

Identify possible security, public safety, political, economic, infrastructure, operational, or community concerns.

7. Confidence Level

Assign High, Medium, or Low confidence. Explain why.

8. Follow Up Questions

List the most important questions the user should research next.

9. 45 Second Brief

Create a short briefing summary that could be read out loud in under 45 seconds.

Rules:
Use only the provided sources.
Do not invent missing details.
If information is missing, state not provided.
Keep the writing clear, useful, and briefable.
Save both files.
Then run:
streamlit run app.py
If it opens, paste a short article or event description into Source 1 and click Generate. If it errors, copy the exact red error text here.
ok lets build the next thing
Thought for 8s
Next build the evaluation pieces because that directly fixes the Project 1 feedback.
Create these files inside Tests:
sample_news_1.txt
sample_news_2.txt
sample_news_3.txt
eval_results.md
Use synthetic test data for now so no real military, private, or sensitive information goes into the project.
Put this in Tests/sample_news_1.txt:
Synthetic test case for TrendLens AI. This is not real news.

A city emergency management office reported increased flooding along several low lying roads after heavy rainfall. Public works crews closed two intersections and advised residents to avoid unnecessary travel in the affected area. No injuries were reported. Officials stated that drainage crews would continue monitoring water levels through the evening.
Put this in Tests/sample_news_2.txt:
Synthetic test case for TrendLens AI. This is not real news.

A regional transportation agency announced temporary delays across several bus routes due to road closures and standing water. The agency stated that service interruptions may continue until conditions improve. Local officials asked commuters to check official updates before traveling.
Put this in Tests/sample_news_3.txt:
Synthetic test case for TrendLens AI. This is not real news.

A local hospital network issued a public notice reminding patients to allow extra travel time because several routes near its main campus were affected by weather related traffic delays. The notice stated that emergency services remained operational, but some outpatient appointments could experience delays.
Now put this in Tests/eval_results.md:
# TrendLens AI Evaluation Results

## Purpose

This file documents early evaluation testing for TrendLens AI. The goal is to show whether the application produces structured situational awareness products that provide value beyond a basic chatbot summary.

## Test Case 1: Local Flooding and Transportation Disruption

### Input Sources

The test used three synthetic public information style sources:

1. City emergency management update about flooding and road closures
2. Regional transportation update about bus delays
3. Hospital network notice about travel delays near a medical campus

### Expected Behavior

The system should:

1. Identify the situation as a local public safety and infrastructure disruption.
2. Connect the sources into one unified situation instead of summarizing them separately.
3. Identify transportation disruption, public safety, and healthcare access as key concerns.
4. Provide a Bottom Line Up Front.
5. Generate a concise executive summary.
6. Explain the “so what” clearly.
7. Identify key trends across the sources.
8. Provide a confidence level.
9. Generate useful follow up questions.
10. Provide a short 45 second brief.

### Actual Output

Paste the actual TrendLens AI output here after running the test.

### Pass or Fail

Pending.

### Notes for Improvement

Pending actual test output.
Then commit it:
git add .
git commit -m "Added initial evaluation test cases"
git push
After that, the next smart thing is to run the app with these three samples, copy the actual report into eval_results.md, mark what passed or failed, then commit again. That will show real evaluation evidence instead of just planned testing.
wait lets build a Tests/ sample_news_3.txt Synthetic test case for TrendLens AI. This is not real news. A UAS was shot down over the Atropia white house linked to Ariana. Atropia in response striked down a UAS ground operations factory and eight one way UAS that were in route toward government buildings and the embassy. Test/ sample_news_4.txt Synthetic test case for TrendLens AI. This is not real news. Limaria has come to an agreement on peace talks after the last four years of negotiations over nuclear programs and the storage of chemicals of mass destruction regulations implemented by the Farnovian government. Test/ sample_news_5.txt Synthetic test case for TrendLens AI. This is not real news. Wildfires have put thousands displaced from their homes as FEMA and firefighters from across the country attempt to contain the fires in Philconia. Animal Rescues also assist with relocating wildlife, farm animals, and pets. Test/ sample_news_6.txt Synthetic test case for TrendLens AI. This is not real news. The Drasta company has created a new low cost nutrient dense crop that can grow in almost any environment. The crop is a called Susu and grows in clusters underground. Drasta has employed tens of thousands of new workers to train farmers and those in remote areas around the world on proper irrigation and low cost farming tools to help deploy the crop. I also have a fake news video too if we need for later
Thought for 7s
Yes, these are good. They give the app different event types to test:
local or international security event
 diplomatic negotiation event
 natural disaster and humanitarian response event
 food security and economic development event
Use Tests, not Test, so the folder matches what is already in your project.
Create these files inside the Tests folder.
Tests/sample_news_3.txt
Synthetic test case for TrendLens AI. This is not real news.

A UAS was intercepted over a government compound in Atropia. Officials linked the activity to Ariana. In response, Atropia reported strikes against a UAS ground operations facility and eight one way UAS that were en route toward government buildings and the embassy. Officials stated that the incident remains under review.
Tests/sample_news_4.txt
Synthetic test case for TrendLens AI. This is not real news.

Limaria has agreed to resume peace talks after four years of negotiations involving nuclear program oversight and chemical weapons storage regulations implemented by the Farnovian government. Officials stated that the talks are intended to reduce regional tension and establish clearer monitoring procedures.
Tests/sample_news_5.txt
Synthetic test case for TrendLens AI. This is not real news.

Wildfires in Philconia have displaced thousands of residents from their homes as FEMA and firefighters from across the country attempt to contain the fires. Animal rescue groups are also assisting with the relocation of wildlife, farm animals, and pets affected by the fires.
Tests/sample_news_6.txt
Synthetic test case for TrendLens AI. This is not real news.

The Drasta company has created a new low cost nutrient dense crop that can grow in many environments. The crop is called Susu and grows in clusters underground. Drasta has employed tens of thousands of workers to train farmers and remote communities on irrigation methods and low cost farming tools to help deploy the crop.
For now, keep the fake news video as a later expansion. The Sunday draft should focus on pasted text sources first. Video ingestion would add too much complexity unless the professor specifically wants multimodal work.
After saving those files, commit them:
git add .
git commit -m "Added additional synthetic event test cases"
git push
Next smart step after this is updating eval_results.md so it explains what each test case is supposed to prove.
Your next 48 hours should be:
Day 1:
 Clean app.py
 Clean trend_tools.py
 Finalize system prompt
 Generate one strong sample report
 Update README
Day 2:
 Test with 2 or 3 real public articles
 Take screenshots
 Write build log
 Write limitations and future work
 Prepare short demo explanation
Your professor’s scope question is answered by saying:
I narrowed TrendLens AI to focus on ingesting multiple public sources and harmonizing them into one structured intelligence summary, instead of trying to combine multi source ingestion, tool calling, and autonomous agents all at once.
what questions do you have for me? ok I will test after we go over everything first what do I currently need still and what do I have to get the draft done
Based on where you are right now, I would not write any more code until we answer a few architecture questions. The biggest risk is spending hours coding something that later doesn't fit the project requirements.
The questions I have are:
What is the actual input?
Right now I have heard:
 • URLs
 • pasted article excerpts
 • news summaries
 • public event descriptions
Which one is the primary input?
My recommendation:
 Allow both URLs and pasted text.
That gives you flexibility during the demo if a website blocks scraping.
What is the actual output?
Right now I think it is:
Executive Summary
Key Trends
Risks and Concerns
Confidence Assessment
Recommended Follow Up Questions
Do you want anything else?
Because "Intelligence Summary" can mean many things.
For example, military analysts often want:
 • BLUF (Bottom Line Up Front)
 • Key Judgments
 • Indicators
 • Assessment
 • Collection Gaps
Corporate users may want:
 • Trends
 • Opportunities
 • Risks
We should decide now.
Who is the target user?
This is a huge question.
Is TrendLens for:
• Intelligence analysts?
 • Business leaders?
 • Students?
 • Emergency managers?
 • General public?
My recommendation:
Situational awareness analysts.
That is broad enough to cover intelligence, cybersecurity, emergency management, and business risk monitoring.
Does the AI compare sources?
This could become a great feature.
Example:
Source A says escalation is increasing.
Source B says tensions are decreasing.
TrendLens could identify:
"Conflicting reporting exists between sources regarding escalation trends."
That looks sophisticated while being relatively easy to implement.
What makes TrendLens different from ChatGPT?
This question will absolutely come up during grading.
You need an answer.
Possible answer:
TrendLens provides a structured intelligence workflow that transforms multiple public information sources into a standardized situational awareness product with confidence assessments and follow up collection requirements.
In other words:
ChatGPT = general assistant
TrendLens = intelligence reporting assistant
Is the "agent" real or simulated?
Be honest.
Most student projects do not need real autonomous agents.
I would use:
Source Intake Agent
Trend Extraction Agent
Risk Assessment Agent
Report Generation Agent
Even if they are just sequential prompt steps.
That still demonstrates agentic workflow.
Right now, looking at your repository, I think you already have about 70% of the project.
What I think you already have:
 ✅ GitHub repository
 ✅ Streamlit application
 ✅ Project concept
 ✅ Output folder
 ✅ Prompt structure
 ✅ Report generation logic
 ✅ Basic workflow
What I think you still need:
🔲 Final project statement (one sentence)
🔲 Final report format
🔲 README cleanup
🔲 Example input dataset
🔲 Example output report
🔲 Screenshots
🔲 Build log
🔲 Future work section
🔲 Evaluation section
🔲 Testing against 2 to 3 real world events
If those boxes are checked, you likely have a complete draft.
The single most important question I would like answered before touching any code is:
"When I demonstrate TrendLens to the professor, what exact information does the user enter and what exact report do they receive?"
Once that is locked down, everything else becomes much easier.
1. Yes I need flexibility for the user since many times sources can be varied for inputs and come from different types of sources. right now I believe we have spots for 3 different sources to input/ upload/ or paste text inputs and I will need to ensure there is not a limit to how few or how many sources can be uploaded or included (or possibly up to 10 documents at a single time uploaded at once before having the ability to upload more if needed or include additional inputs if pushback is needed or additional asks are requested giving the user as much control as possible. Also include boxes that give the user some ideas to what can be requested as an output since sometimes users don't know what they can request if just given a box to insert text into or something 2. For the output I want boxes to check for what the individual wants to include for the output so they can select what output they recieve and leave a text box for other inputs for asking what output is wanted by the user to give the user the most control. Output box options could include conditions, circumstances, and influences The 5 Ws Safety considerations The so what or why this matters (ask user for who the audience is or who this brief is tailored to 2nd order effects 3rd order effects Executive Summary Key Trends Risks and Concerns Confidence Assessment (identify and explicitly explain the percentages and what they mean for confidence assessment) BLUF (Bottom Line Up Front) • Key Judgments • Indicators • Assessment • Collection Gaps output options also should include a GRINTSUM (Graphical Intelligence Summary) with images or graphs/ tables/ charts or include these broken up into the buttons as additional options Recommended Follow Up Questions Is this acceptable for this product or are there any other uncommon considerations I have not thought of yet? 3. Target user is Intelligence Analysts however, often times they utilize information that is not just open source but classified information so we are only focusing on publically available information at this time. The other users could be emergency managers, or the general public and students as other adaptors of the application I want to make it towards Intelligence Analysts but offer features that other secondary users can adopt as well. I would like to ask the user in a drop down format what their role is or something so people can have this really customized based on their position, role, or their current intent for use based on who they are 4. AI will need to compare sources yes. This is crucial for proper analysis. 5. We will also need to make this semi autonomous where it searches in the background and on its own to check for continued updates as stories and events develop to ensure users or notified if the articles or the events being tracked are changing TrendLens provides a structured intelligence workflow that transforms multiple public information sources into a standardized situational awareness product with confidence assessments and follow up collection requirements. 6. The agent needs to be real autonomous agents how do I implement using Source Intake Agent, Trend Extraction Agent? What other are best here and do agents only provide one function? If so how many agents will I need can I just use one now and develop further so the scope remains within grasp? ok lets focus on the above and then later we can move to Final project statement (one sentence) 🔲 Final report format 🔲 README cleanup 🔲 Example input dataset 🔲 Example output report 🔲 Screenshots 🔲 Build log 🔲 Future work section 🔲 Evaluation section 🔲 Testing against 2 to 3 real world events
Thought for a couple of seconds
Yes, this is acceptable, but it is too much for the first working draft unless it is organized into “now” and “later.”
The main decision should be:
For this week, TrendLens AI should focus on multi source intake, source comparison, and a structured intelligence summary.
Everything else can be designed into the interface as future ready, but only a smaller set needs to work right now.
Current version goal
TrendLens AI should allow users to paste or upload multiple public sources, select their role, choose the desired report sections, and generate one structured situational awareness product.
What to build now
Flexible source input
Keep 3 visible source boxes for simplicity, but add a note that the user can add more sources later or paste multiple sources into one box. If you can code it quickly, add an “add another source” pattern. If not, keep the 3 boxes and say future development supports up to 10 source uploads.
For this week, do not actually build unlimited uploads unless the app already supports it.
Add source types
Let the user label each input as:
Article
Government source
Social media post
Report
Field note
Other public source
This helps the AI understand how to treat the information.
Role dropdown
Add a dropdown like:
Intelligence Analyst
Emergency Manager
Student
Business Leader
General Public
Other
Then add a text box:
“What is the purpose of this report?”
Example:
Prepare a commander update
Understand public safety risk
Summarize a developing event
Compare conflicting sources
Create a student research summary
Output checkboxes
This is a good idea. For the first working draft, include the most useful checkboxes:
BLUF
Executive Summary
5 Ws
Key Judgments
Key Trends
Conditions, circumstances, and influences
Risks and concerns
Safety considerations
Second order effects
Third order effects
Indicators
Assessment
Collection gaps
Confidence assessment
Recommended follow up questions
For GRINTSUM, do not promise full image generation yet. Call it:
Graphical Summary Table
That can be a structured table or chart layout inside the report. Full maps, images, and generated graphics can go under future work.
Confidence assessment
Yes, include it. This makes the project stronger.
Use simple percentage bands:
High confidence: 80 to 100 percent. Multiple reliable sources agree, details are consistent, and major facts are supported.
Moderate confidence: 50 to 79 percent. Some source agreement exists, but gaps, unclear details, or limited reporting remain.
Low confidence: 0 to 49 percent. Reporting is limited, conflicting, early, or difficult to verify.
Also make the AI explain why it chose that confidence level.
Source comparison
This is crucial and should be part of the main project.
Add a section called:
Source Comparison and Reliability Notes
It should identify:
Where sources agree
Where sources conflict
What details are missing
Which claims need confirmation
Whether the event appears to be developing
This is one of the strongest parts of your project because it makes TrendLens different from a basic summarizer.
Semi autonomous update tracking
This is a good idea, but not for this week unless everything else is finished.
For now, include it as future work:
Future versions of TrendLens AI could include background monitoring that periodically checks public sources for new developments and notifies users when a tracked event changes.
That sounds strong without overbuilding.
Agents
For this project, use one main agent now with clearly defined internal workflow steps.
Do not build 6 real autonomous agents this week.
Use:
TrendLens Analysis Agent
Inside that agent, describe the workflow:
Source Intake
Source Normalization
Source Comparison
Trend Extraction
Risk and Impact Assessment
Confidence Assessment
Report Generation
This keeps the scope realistic but still shows agentic thinking.
Later, you can split these into separate agents:
Source Intake Agent
Source Comparison Agent
Trend Extraction Agent
Risk Assessment Agent
Confidence Assessment Agent
Report Generation Agent
Update Monitoring Agent
For now, one agent is enough.
Do agents only provide one function?
Not always. An agent can have one narrow job, or it can manage a workflow with several steps. For this project, the safest approach is one agent with multiple structured functions. That is easier to explain and easier to code.
What you currently need to get the draft done
You need the app to show:
Input section
Role dropdown
Purpose text box
Source input boxes
Output checkbox section
Generate report button
Structured report output
Save report button or output saved to folder
You need the README to explain:
What TrendLens AI does
Who it is for
What the narrowed scope is
What AI techniques are used
What the agent workflow is
What the limitations are
What future work includes
You need one sample report showing:
3 public sources entered
Selected role
Selected output sections
Final intelligence style product
Source comparison
Confidence assessment
Recommended follow up questions
My recommendation for the draft
Do not chase full autonomy yet.
Build the strongest possible version of:
Multiple public inputs plus customized intelligence style output plus source comparison plus confidence assessment.
That is enough for a solid Project 2 and it directly answers your professor’s concern.


Your next best order is:
Update README.md first.
 Update app.py second.
 Create monitoring.py third.
 Create scheduler_worker.py fourth.
 Update trend_tools.py fifth.
 Run one test with changed source text.
 Save the output.
 Update BUILD_LOG.md and Tests/eval_results.md.
 Commit and push.
What is next 

Yes, this is meeting the working draft requirement so far.
It shows a clear direction, a working Streamlit interface, role based customization, source intake, selectable report sections, a visible agent workflow, and tool use through helper functions. Your Git history also shows the recent commits and push were successful, including the prompt structure and updated workflow, and your last status showed a clean working tree.
The stronger answer is: yes, but it still needs three things before it feels safe for the Project 2 draft checkpoint.
You need to prove the app actually generates a report
Right now the interface is visible, but the screenshot text shows “Valid sources detected: 0.” That is fine before testing, but for submission you need at least one completed run.
Next action:
Paste two public source excerpts into Source 1 and Source 2.
Use this purpose:
Compare public reporting on a developing event and create a short situational awareness update.
Then generate a report and make sure it includes:
Source Overview
BLUF
So What or Why This Matters
Source Comparison and Reliability Notes
Confidence Assessment
45 Second Brief
Once it generates, save the output to the Outputs folder and commit it.
You need a build log
This directly responds to the Project 1 feedback. The instructor already told you that a missing build log cost points before. For Project 2, add a file like:
BUILD_LOG.md

It should document what changed, why it changed, and what you learned.
Example entries:
May 28, 2026: Created initial Streamlit app structure with public source input boxes and basic report generation.
May 29, 2026: Added OpenAI integration, Prompts folder, report saving, and feedback logging.
May 30, 2026: Narrowed project scope based on instructor feedback from a broad agentic public event monitor to a focused multi source intelligence summary generator.
May 30, 2026: Added role based customization, selectable report sections, Source Overview, So What, Source Comparison, Confidence Assessment, and 45 Second Brief.
May 30, 2026: Updated trend_tools.py so the report prompt receives user role, report purpose, selected outputs, and custom user requests.
May 30, 2026: Added report_prompt.md and system_prompt.md to separate system behavior from report structure.
This alone will protect you from the same Project 1 issue.
You need test results, not just test files
The Project 1 feedback said the tests folder needs actual evaluation output or pass fail results. So for this draft, create or update:
Tests/eval_results.md

Include something like this:
# TrendLens AI Evaluation Results

Test 1: Two related public safety sources

Input type: Two pasted article excerpts  
Role: Intelligence Analyst  
Purpose: Compare reporting and create a situational awareness update  
Expected result: Report identifies shared facts, missing details, risks, and confidence level  
Result: Pass  
Notes: Report produced BLUF, Source Overview, Source Comparison, Confidence Assessment, and Follow Up Questions.

Test 2: One source only

Input type: One pasted public source  
Role: Student  
Purpose: Summarize and explain why the event matters  
Expected result: Report avoids inventing missing source comparison  
Result: Pass  
Notes: Report stated limited confidence because only one source was available.

Test 3: Unrelated sources

Input type: Three unrelated public source excerpts  
Role: General Public  
Purpose: Identify whether the sources connect  
Expected result: Report should not force a false narrative  
Result: Pass  
Notes: Report separated themes and identified that the sources were not directly connected.

This shows evaluation, not just code.
For the “value beyond ChatGPT” part
This is the most important part of the professor’s old feedback. Your project needs to clearly show why this is more useful than a basic chat session.
Your answer should be:
TrendLens AI is not just a chat box. It gives the user a structured intelligence workflow with source labeling, role selection, report purpose, selectable output sections, source comparison, reliability notes, confidence assessment, follow up questions, and a saved report output. The user does not need to know how to prompt the model correctly because the application guides the analysis process.
That is the value.
One concern from what you pasted
The checkbox section in your pasted text looks blank under “Select Desired Report Sections.” In the actual browser, do you see the checkbox labels, or are they visually missing?
If the actual browser shows the labels, it is fine.
If the actual browser really looks blank, we need to fix the checkbox layout before moving forward because that hurts usability.
Your next best step
Run one successful test report now. Then commit the generated report and test evaluation.
Use:
streamlit run app.py

After the report works, run:
git add Outputs Tests BUILD_LOG.md README.md
git commit -m "Add build log and evaluation results"
git push

After that, your draft will be much stronger for the Project 2 checkpoint.


Ok don’t forget to add this to the GITHUB prompts info! 

i think I used Python 3.14 is that bad can I still change it somehow?
Thought for 5s
It is not “bad,” but it can cause dependency issues. Your app uses common packages, so it might still work, but Python 3.12 is the safer choice for Streamlit Community Cloud.
Streamlit’s own docs say Python version is selected in Advanced settings during deployment, and Python itself cannot be changed after deployment. To change it, the official process is to delete the deployed app and redeploy it with the correct Python version selected.
Do this:
Go to your Streamlit app dashboard.
Delete the deployed app that is using the wrong setup.
Create a new app.
Enter the correct deployment settings:
Repository:
https://github.com/LindseyB1/TrendLens_AI

Branch:
main

Main file path:
app.py

App URL:
trendlens-ai-britney
or another available name like:
trendlens-sitrep
trendlens-watch
trendlens-brief
Open Advanced settings.
Change Python version to:
3.12
Streamlit Community Cloud defaults to Python 3.12 and lets users select a version from the Advanced settings dropdown during deployment.
Add your secrets again:
OPENAI_API_KEY = "your_actual_key_here"
OPENAI_MODEL = "gpt-4.1-mini"
Click Save.
Click Deploy.
Before hitting deploy, double check these three things:
Branch must be main
Main file path must be app.py
Python version should be 3.12
Your repo is already pushed and clean, so deleting and redeploying the Streamlit app will not hurt your code.
ok lets try again
Thought for 8s
Yes, what you pasted looks like the app is loading correctly. Valid sources detected: 0 is normal right now because no source text has been pasted yet.
Now make sure these parts work before submitting.
Generate Report tab
Test this first because it is the main feature.
Use this report purpose:
Compare public reporting on a developing event and create a short situational awareness update.
Paste this into Source 1:
City officials reported a chemical spill near an industrial facility. Roads near the facility were closed while crews assessed the scene.
Paste this into Source 2:
Fire officials confirmed that two nearby businesses were evacuated as a precaution. The county emergency management office issued public guidance for the public to avoid the area.
Then click:
Generate TrendLens Report
Make sure the report includes several of these:
Source Overview
Bottom Line Up Front
Executive Summary
Source Comparison and Reliability Notes
Confidence Assessment
Follow Up Questions or RFIs
Save Report button
After the report generates, click:
Save Report
Make sure it gives a success message and shows a saved file path.
This proves the app can take an action, not just generate text.
Download Report as Markdown
Click:
Download Report as Markdown
Make sure it downloads a .md file.
This is helpful because your professor can see the output even if the saved file path is only inside the hosted app environment.
Feedback section
Enter something like:
The report was useful and included source comparison, but it could explain confidence more clearly.
Then click:
Save Feedback
Make sure it saves successfully.
This proves the feedback logging part works.
Monitoring Workflow tab
Go to the Monitoring Workflow tab.
Test the manual change detection.
Previous source text:
City officials reported a chemical spill near an industrial facility. Roads near the facility were closed while crews assessed the scene.
Updated source text:
City officials reported a chemical spill near an industrial facility. Roads near the facility were closed while crews assessed the scene. Fire officials confirmed that two nearby businesses were evacuated as a precaution. The county emergency management office issued public guidance to avoid the area.
Click:
Compare Source Text
Make sure it shows:
changed: true
meaningful_change: true
or something close to that.
Save Monitoring Topic
In the Monitoring Workflow tab, save a sample topic like:
Chemical spill public safety updates
Monitoring purpose:
Track public updates and identify meaningful changes in official guidance, evacuations, road closures, or reported impacts.
Leave the interval at:
5
Click:
Save Monitoring Topic
Make sure it saves.
About tab
Open the About tab and make sure it explains:
agentic AI system
tool based actions
feedback logging
semi automated monitoring
model routing
MCP style architecture
data safety notice
Streamlit deployment card
On Streamlit Cloud, make sure the app says:
main · app.py
Not:
main · monitoring.py
Secrets
Make sure the Streamlit secrets are set like this:
OPENAI_API_KEY = "your actual key"
OPENAI_MODEL = "gpt-4.1-mini"
Do not put your key in GitHub.
GitHub repo
Make sure GitHub has these files:
README.md
app.py
trend_tools.py
monitoring.py
scheduler_worker.py
requirements.txt
Prompts/
Tests/
Outputs/
Monitoring/
Final documentation still needed
After testing the app, your next project files to update are:
BUILD_LOG.md
Tests/eval_results.md
For the submission, you should have:
Live Streamlit app link
GitHub repository link
Screenshot of the app loaded
Screenshot of one generated report
Saved output report
Build log
Evaluation results
The next best step is to run one full report test now, download or save the output, then update BUILD_LOG.md and Tests/eval_results.md.
Pasted text(146).txt
Document
 wow this app is really good I am impressed with the features and outputs it really works great job . How does it have an agent running to help the user by providing alerts or updates to the user should the people have to login to save the history or should it email them any updates it finds?
Thought for 15s
The app is working really well as a working draft. Right now, it has the foundation of an agentic workflow: it accepts a user role, purpose, source text, selected outputs, routes the task, generates a report, saves outputs, saves feedback, and includes a monitoring workflow tab for change detection. Your test output shows the app successfully generated an analyst style report from one weather source and adjusted the output to the Intelligence Analyst audience.
For alerts and updates, here is the cleanest answer:
Right now, TrendLens AI has a monitoring agent design, but not a fully live alerting agent yet.
What it currently has:
The user can enter a monitoring topic.
The app can compare old source text against updated source text.
The system can detect meaningful changes.
The scheduler worker can check whether a topic is due for review every five hours.
The app can save reports and logs.
What it does not fully have yet:
It does not automatically email users.
It does not have user accounts.
It does not have a permanent database.
It does not run a true always on background worker inside Streamlit Cloud.
That last part matters because Streamlit Community Cloud apps go to sleep after 12 hours without traffic, so it is not the best place to run a continuous background alerting agent by itself. Streamlit’s own documentation says sleeping apps can be woken by anyone with access, but that means the app is not guaranteed to keep running background jobs nonstop.
The best design for your class project is this:
Keep the app public with no login for the working draft.
For the professor, no login is better. It removes friction. He can open the link, test the app, generate a report, and see the monitoring workflow.
Add history saving later through a database.
If this became a real product, then users should have accounts so each person can save their own monitored topics, past reports, and alert settings. Without login, everyone shares the same app environment, which is not ideal for personal history.
Add email alerts as an optional future feature.
The best alert design would be:
User creates a monitoring topic.
 User chooses “email me only when meaningful changes are detected.”
 Scheduler checks every five hours.
 If meaningful change is found, the app generates an updated report.
 The system saves the report and emails a short alert with a link back to the app.
Do not email every check. Only email meaningful changes. Otherwise it becomes spammy.
For your README or project explanation, use this wording:
TrendLens AI currently includes a semi automated monitoring workflow. The user can save a public topic, compare previous and updated source text, and identify meaningful changes. The scheduler worker supports a five hour review cycle. In the current working draft, alerts are represented through saved monitoring logs and change detection results. A future version would connect the scheduler worker to a database and optional email notification service so users can receive alerts when meaningful changes are detected.
Best next version:
No login for professor testing.
Optional login for real user history.
Optional email alerts only for meaningful changes.
Database needed for reliable long term saved history.
External scheduler needed for true five hour checks.
For deployment, keep Streamlit as the user interface, but treat the alert agent as a separate worker. The architecture would be:
Streamlit app = user interface
monitoring.py = change detection tool
scheduler_worker.py = five hour review worker
trend_tools.py = report generation tool
database = saved topics and report history
email service = alert delivery
That is a strong agentic system explanation because it shows reasoning, tools, memory, feedback, and limited autonomy.

