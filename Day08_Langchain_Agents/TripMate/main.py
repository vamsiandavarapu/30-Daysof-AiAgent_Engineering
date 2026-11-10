
import os
import unicodedata
import requests
from datetime import datetime
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from xml.sax.saxutils import escape

load_dotenv()

# 1. WEATHER TOOL
@tool
def get_weather(city: str, date: str):
    """Get weather forecast for a city. Date format: YYYY-MM-DD."""
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric"
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    forecasts = response.json()["list"]

    results = [
        {
            "time": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "weather": item["weather"][0]["description"],
            "rain_probability": item.get("pop", 0)
        }
        for item in forecasts
        if item["dt_txt"].startswith(date)
    ]

    return results if results else "Forecast unavailable for this date."


# 2. WEB SEARCH TOOL
@tool
def web_search(query: str):
    """Search the web for travel attractions, restaurants and local experiences."""
    response = requests.post(
        "https://google.serper.dev/search",
        headers={
            "X-API-KEY": os.getenv("SERPER_API_KEY"),
            "Content-Type": "application/json"
        },
        json={"q": query},
        timeout=20
    )

    response.raise_for_status()
    data = response.json()

    return [
        {
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "link": item.get("link")
        }
        for item in data.get("organic", [])[:6]
    ]


# 3. CREATE LANGCHAIN AGENT
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2
)

agent = create_agent(
    model=model,
    tools=[get_weather, web_search],
    system_prompt="""
    You are TripMate, a travel planning assistant.

    Create practical day-wise travel itineraries.
    Use web search to research attractions and experiences.
    Use weather forecasts for the requested travel dates.

    Weather must influence your decisions:
    - Rain: prefer indoor activities.
    - High temperatures: schedule outdoor activities
      during cooler hours.
    - Suitable weather: consider outdoor activities.

    Never invent weather information, prices or opening hours.
    Clearly mention when forecast information is unavailable.
    Explain why activities suit the weather.
    Consider the user's budget and number of travelers.
    Return a clear, detailed itinerary with estimated costs.
    """
)


# 4. BASIC PDF GENERATION
def generate_pdf(content):
    os.makedirs("generated_pdfs", exist_ok=True)

    filename = datetime.now().strftime(
        "generated_pdfs/TripMate_%Y%m%d_%H%M%S.pdf"
    )

    styles = getSampleStyleSheet()
    document = SimpleDocTemplate(filename, pagesize=A4)

    content = content.translate(str.maketrans({"₹": "INR ", "–": "-", "—": "-", "‑": "-", "•": "-"}))
    content = unicodedata.normalize("NFKD", content).encode("ascii", "ignore").decode()
    lines = [
        line.strip().replace("**", "").replace("`", "").replace("|", " | ")
        for line in content.splitlines()
        if line.strip() and not set(line.strip()) <= set("|-: ")
    ]
    elements = [
        Paragraph("TripMate - Travel Itinerary", styles["Title"]),
        Spacer(1, 20),
        *[
            Paragraph(
                escape(line.lstrip("# >")),
                styles["Heading2"] if line.startswith("#") else styles["BodyText"]
            )
            for line in lines
        ],
    ]

    document.build(elements)
    return filename


# 5. MAIN PROGRAM
def main():
    print("\nWelcome to TripMate!")
    print("Describe your travel plan in natural language.")
    print("Type 'exit' to quit.\n")

    while True:
        prompt = input("You: ").strip()

        if prompt.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if not prompt:
            continue

        print("\nTripMate is planning your trip...\n")

        result = agent.invoke({
            "messages": [{"role": "user", "content": prompt}]
        })

        itinerary = result["messages"][-1].content

        print("\n========== TRIPMATE ITINERARY ==========\n")
        print(itinerary)

        approval = input(
            "\nDo you want to generate a PDF? (yes/no): "
        ).strip().lower()

        if approval == "yes":
            path = generate_pdf(itinerary)
            print(f"\nPDF generated: {path}")
        else:
            print("\nPDF generation skipped.")

        print("\n" + "-" * 50)

if __name__ == "__main__":
    main()
