from dotenv import load_dotenv
import os

load_dotenv()

WEATHER_API_KEY=os.getenv("WEATHER_API_KEY")

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

ORS_API_KEY=os.getenv("ORS_API_KEY")

TRAFFIC_API_KEY=os.getenv("TRAFFIC_API_KEY")