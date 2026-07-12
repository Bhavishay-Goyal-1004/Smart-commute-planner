import requests
from config import TRAFFIC_API_KEY
from datetime import datetime

BASE_URL = "https://api.tomtom.com/routing/1/calculateRoute"


def get_traffic(start, end):
    """
    Fetch live traffic information from TomTom.

    start = [longitude, latitude]
    end   = [longitude, latitude]
    """

    start_str = f"{start[1]},{start[0]}"
    end_str = f"{end[1]},{end[0]}"

    url = (
        f"{BASE_URL}/{start_str}:{end_str}/json"
        f"?traffic=true"
        f"&travelMode=car"
        f"&key={TRAFFIC_API_KEY}"
    )

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    data = response.json()

    summary = data["routes"][0]["summary"]

    # Live travel time (minutes)
    traffic_time = round(summary["travelTimeInSeconds"] / 60)

    # Delay due to traffic (minutes)
    delay = round(summary.get("trafficDelayInSeconds", 0) / 60)

    # Congestion based on delay
    if delay <= 5:
        congestion = "Low"
    elif delay <= 15:
        congestion = "Moderate"
    elif delay <= 30:
        congestion = "Heavy"
    else:
        congestion = "Severe"

    return {
        "traffic_time": traffic_time,
        "delay": delay,
        "congestion": congestion
    }

def get_peak_hour(congestion):
    """
    Returns peak hour status based on current time and traffic congestion.
    """

    now = datetime.now()

    hour = now.hour

    if 7 <= hour < 11:
        period = "🌅 Morning Peak"

    elif 12 <= hour < 16:
        period = "☀️ Afternoon Peak"

    elif 17 <= hour < 21:
        period = "🌇 Evening Peak"

    elif 21 <= hour or hour < 7:
        period = "🌙 Night"

    else:
        period = "☀️ Off Peak"

    return f"{period} ({congestion} Traffic)"