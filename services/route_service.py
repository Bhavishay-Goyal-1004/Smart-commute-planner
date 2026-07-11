import requests
from config import ORS_API_KEY

GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"
DIRECTIONS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


def get_coordinates(place):
    """
    Returns:
    (longitude, latitude)
    """

    headers = {
        "Authorization": ORS_API_KEY
    }

    params = {
        "text": place,
        "size": 1
    }

    response = requests.get(
        GEOCODE_URL,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if not data["features"]:
        raise ValueError(f"Location not found: {place}")

    coordinates = data["features"][0]["geometry"]["coordinates"]

    return coordinates


def get_route(source, destination):
    """
    Returns:
    {
        distance,
        travel_time,
        start,
        end
    }
    """

    start = get_coordinates(source)
    end = get_coordinates(destination)

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            start,
            end
        ]
    }

    response = requests.post(
        DIRECTIONS_URL,
        json=body,
        headers=headers,
        timeout=15
    )
    print("Status Code:", response.status_code)
    print("Response:")
    print(response.text)

    response.raise_for_status()

    route = response.json()["routes"][0]["summary"]

    return {
        "distance": round(route["distance"] / 1000, 2),
        "travel_time": round(route["duration"] / 60),
        "start": start,
        "end": end
    }