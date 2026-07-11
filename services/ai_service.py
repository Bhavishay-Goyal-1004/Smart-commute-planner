from config import GEMINI_API_KEY
from google import genai
import json

API_KEY = GEMINI_API_KEY

if not API_KEY:
    print("API Key not found!")
    exit()

# Gemini Client
client = genai.Client(api_key=API_KEY)


PLAN_PROMPT = """
You are an AI Smart Commute Assistant.

Analyze the following commute information and provide practical, concise travel advice.

Commute Details:
- Source: {source}
- Destination: {destination}
- Distance: {distance}
- Estimated Travel Time: {travel_time}
- Weather: {weather}
- Temperature: {temperature}°C
- Humidity: {humidity}%
- Wind Speed: {wind_speed} km/h
- Visibility: {visibility} km
- Traffic Level: {traffic}
- Fuel Cost: ₹{fuel_cost}

Based on this information, provide:

1. Best Departure Time
   - Should the user leave now, earlier, or later?
   - Mention if traffic or weather affects the timing.

2. Safety Advice
   - Mention precautions based on the weather and traffic conditions.

3. Packing Suggestions
   - Suggest useful items to carry (umbrella, water bottle, jacket, sunglasses, raincoat, etc.) only if relevant.

4. Travel Tips
   - Give 2–3 practical tips to make the commute smoother.

Rules:
- Return ONLY a valid JSON object.
- Do not include markdown, code fences (```), explanations, or any text before or after the JSON.
- Use this exact structure:

{{
    "departure": "...",
    "safety": "...",
    "packing": "...",
    "tips": [
        "...",
        "...",
        "..."
    ]
}}

- Keep each value concise (1–2 sentences).
- Give exactly 3 travel tips.
- Do not repeat the input values.
- Do not make assumptions beyond the provided data.
- If conditions are normal, reassure the user that the trip looks comfortable.
"""


def get_info(source, destination, weather_data, distance,fuel_cost, traffic, travel_time):

    prompt = PLAN_PROMPT.format(
        source=source,
        destination=destination,
        distance=distance,
        travel_time=travel_time,
        weather=weather_data["condition"],
        temperature=weather_data["temperature"],
        humidity=weather_data["humidity"],
        wind_speed=weather_data["wind_speed"],
        visibility=weather_data["visibility"],
        traffic=traffic["congestion"],
        fuel_cost=fuel_cost,
    )

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown if Gemini adds it
        if text.startswith("```json"):
            text = text[7:]

        if text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        return json.loads(text)

    except Exception as e:

        print("Gemini Error:", e)

        return {
            "departure": "Not available",
            "safety": "Not available",
            "packing": "Not available",
            "tips": [
                "Unable to generate AI suggestions."
            ]
        }