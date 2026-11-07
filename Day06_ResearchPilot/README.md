# ResearchPilot

ResearchPilot is a command-line research assistant built with LangChain and Groq. It can search the web for current or specific facts, turn search results into a structured research report, and optionally email the report.

## Features

- Decides whether a question needs a web search.
- Searches Google through the Serper API.
- Produces a report with a summary, key findings, and source links.
- Keeps conversation context while the program is running.
- Optionally sends the report by email through Gmail.

## Requirements

- Python
- A Groq API key
- A Serper API key
- Gmail address and app password only if you want to send reports by email

## Setup

Open a terminal in this folder and install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in this folder with your own credentials:

```dotenv
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
GMAIL_ADDRESS=your_gmail_address
GMAIL_APP_PASSWORD=your_gmail_app_password
```

The Gmail settings are optional unless you choose to email a report. Never commit your `.env` file or share its credentials.

## Run

```powershell
python main.py
```

Ask a research question at the prompt. Type `clear` to reset the conversation or `exit` to quit. After a research report is generated, the assistant asks whether you want to email it.

## Project files

- `main.py` — command-line flow, search orchestration, report generation, and conversation loop.
- `tools.py` — Serper-backed Google Search tool.
- `prompts.py` — prompts for deciding when to search and generating reports.
- `schemas.py` — Pydantic models for research reports and sources.
- `memory.py` — in-memory conversation history.
- `email_service.py`, `email_template.py` — optional Gmail delivery and HTML formatting.
- `config.py` — environment variable validation and Groq model configuration.
