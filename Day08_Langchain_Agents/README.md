# Day 8: LangChain Agents

This day contains two examples of LangChain agents:

- `01_Agent_Basic.py` — a math assistant that uses addition and multiplication tools.
- `TripMate/` — a travel-planning assistant that researches attractions, checks weather forecasts, and can save an itinerary as a PDF.

## Requirements

- Python 3.10 or later
- A Groq API key
- A Serper API key for TripMate web searches
- An OpenWeatherMap API key for TripMate forecasts

## Setup

From the `Day08_Langchain_Agents` directory, create and activate a virtual environment and install TripMate's dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r TripMate\requirements.txt
```

Create a `.env` file in the `Day08_Langchain_Agents` directory:

```dotenv
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
OPENWEATHER_API_KEY=your_openweathermap_api_key
```

Keep your real API keys private. The `.env` file is ignored by Git.

## Run the basic math agent

From the `Day08_Langchain_Agents` directory:

```powershell
python 01_Agent_Basic.py
```

The example asks the agent to add two numbers and multiply the result.

## Run TripMate

From the `Day08_Langchain_Agents` directory:

```powershell
python TripMate\main.py
```

Describe a trip in natural language, including the destination and dates. TripMate can use web search for attractions and a weather forecast to guide its itinerary. It asks whether you want to generate a PDF after each itinerary; generated PDFs are saved under `TripMate\generated_pdfs\` and are not tracked by Git.

Type `exit` or `quit` to close TripMate.
