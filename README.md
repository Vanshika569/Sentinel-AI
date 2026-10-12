SentinelAI — AI-Powered SRE Incident Commander

SentinelAI is a student project that monitors local system resource usage, identifies potential CPU, memory, and disk incidents, retrieves relevant troubleshooting guidance, and uses Google's Gemini API to generate a structured incident diagnosis. It also provides rule-based recovery recommendations for a person to review.

Safety note: SentinelAI provides diagnostic guidance and recommendations. It does not automatically terminate processes, delete files, restart services, or make other system changes.

Features

Local system monitoring: Reads CPU, memory, and disk utilization from the machine running the application.

Threshold-based incident detection: Classifies resource usage as HEALTHY, WARNING, or CRITICAL according to the configured rules.

Runbook retrieval: Selects CPU, memory, or disk troubleshooting text from the local knowledge_base folder using keyword matching.

AI-assisted diagnosis: Sends incident details and retrieved runbook content to Gemini to generate an incident summary, possible causes, investigation steps, safe recovery recommendations, and additional suggestions.

Recovery recommendations: Provides rule-based advice without automatically carrying out remediation.

Streamlit dashboard: Presents resource metrics, incident analysis, and runbook guidance.

Technology stack

Python

Streamlit

psutil

Google Gen AI Python SDK (google-genai)

python-dotenv

Pydantic (for structured incident data)

Project structure

sentinel ai/
├── app.py
├── dashboard.py
├── test_recovery.py
├── test_retriever.py
├── test_diagnosis.py
├── test_gemini_connection.py
├── app/
│   ├── agents/
│   │   ├── alertagent.py
│   │   ├── diagnosis_agent.py
│   │   └── recovery_agent.py
│   ├── models/
│   │   └── incident.py
│   ├── services/
│   │   └── system_monitor.py
│   └── runbook_retriever.py
├── knowledge_base/
│   ├── high_cpu.txt
│   ├── high_memory.txt
│   └── high_disk.txt
├── .env                 # Create locally; do not commit
└── .gitignore

File and folder names can vary slightly if the project has been reorganized since this README was written.

Requirements

Python installed on your computer

Internet access for Gemini API requests

A Gemini API key configured for API access

Setup on Windows PowerShell

Run the commands from the project root folder.

Create and activate a virtual environment (skip creation if the existing .venv is already set up):

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Install the packages used by the project:

python -m pip install streamlit psutil google-genai python-dotenv pydantic

Create a .env file in the project root and add your own Gemini API key:

GEMINI_API_KEY=your_api_key_here

Replace the placeholder with your key. Never commit .env or share your API key. Check that .env is listed in .gitignore before pushing changes to GitHub.

Run SentinelAI

Streamlit dashboard

python -m streamlit run dashboard.py

Open the local URL printed by Streamlit in the terminal. Use the sidebar to explore Overview, Incident analysis, and Runbook guidance. The dashboard reads metrics from the machine on which it is running.

Terminal application

python app.py

This runs the Python monitoring and agent workflow and prints the incident report, AI diagnosis (when Gemini responds), and recovery recommendations.

Run tests

Run these from the project root:

python test_recovery.py
python test_retriever.py
python test_diagnosis.py
python test_gemini_connection.py

test_recovery.py checks the rule-based recovery recommendations.

test_retriever.py checks retrieval of CPU, memory, and disk runbooks without making a Gemini request.

test_diagnosis.py checks the Diagnosis Agent with a sample incident and requires a working Gemini API request for a real AI response.

test_gemini_connection.py sends a minimal request to check whether the configured Gemini API can respond.

The Gemini tests require internet connectivity, a valid API key, and model availability. A temporary 503 UNAVAILABLE response indicates that the request could not be served at that time; it does not by itself prove the application logic is incorrect.

How the workflow works

The system monitor collects CPU, memory, and disk utilization.

The alert agent evaluates the metrics and builds an incident object.

The runbook retriever selects relevant local troubleshooting documentation based on keywords in the incident description.

The diagnosis agent supplies incident details and the retrieved documentation to Gemini, which generates a structured explanation.

The recovery agent returns rule-based recommendations for a human to review.

The dashboard displays metrics and, when triggered, incident analysis results.

Current scope and limitations

Monitoring is limited to host-level CPU, memory, and disk usage; application logs, distributed traces, and remote infrastructure are not automatically monitored.

Runbook retrieval is keyword-based. It does not currently use embeddings, semantic search, or a vector database.

Gemini output is AI-generated and may be incomplete or incorrect. Treat possible causes as hypotheses until evidence confirms them.

The project does not automatically remediate incidents. Review recommendations and obtain appropriate approval before taking action.

API availability, quotas, network connectivity, and model configuration can affect AI diagnosis requests.

Thresholds are simple MVP settings and should be tuned for the target environment before operational use.

Security

Keep .env and API credentials out of Git.

Do not include secrets in screenshots, logs, issue reports, or project documentation.

Review AI-generated recommendations before applying them to a real system.

Project status

SentinelAI is a college-level minimum viable project. The basic recovery recommendations, keyword-based runbook retrieval, Gemini diagnosis, and dashboard workflow have been exercised in the development environment. Additional tests and environment-specific validation are recommended before production use.