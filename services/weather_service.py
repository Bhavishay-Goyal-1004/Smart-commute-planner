from config import WEATHER_API_KEY
import requests

API_KEY = WEATHER_API_KEY
def get_weather(city,coord):

    if not API_KEY:
        print("Weather API key not found.")
        return

    # Weather API
    url=(f"https://api.openweathermap.org/data/2.5/weather?lat={coord[1]}&lon={coord[0]}&appid={API_KEY}&units=metric")

    try: 
        response = requests.get(url,timeout=10)

        if response.status_code != 200:
            print(f"Error {response.status_code}: Invalid city name or API issue.")
            return {
                "city": city.title(),
                "temperature": "N/A",
                "humidity": "N/A",
                "wind_speed": "N/A",
                "condition": "Unavailable",
                "visibility": "N/A"
            }

        data = response.json()

        weather_data = {
            "city": city.title(),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": round(data["wind"]["speed"] * 3.6, 1),
            "condition": data["weather"][0]["description"],
            "visibility": round(data.get("visibility", 0) / 1000, 1)
        }

        return weather_data

    # Handling exceptions

    except requests.exceptions.ConnectionError:
        print("No internet connection.")

    except requests.exceptions.Timeout:
        print("Request timed out.")

    except Exception as e:
        print(f"Something went wrong: {e}")

    # except requests.exceptions.RequestException:
        # return None