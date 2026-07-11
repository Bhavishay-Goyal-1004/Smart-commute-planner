import json
import os

HISTORY_FILE = "data/history.json"
FAVOURITES_FILE = "data/favourites.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as file:
        try:
            return json.load(file)
        except:
            return []


def save_history(data):
    with open(HISTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_favourites():
    if not os.path.exists(FAVOURITES_FILE):
        return []

    with open(FAVOURITES_FILE, "r") as file:
        try:
            return json.load(file)
        except:
            return []


def save_favourites(data):
    with open(FAVOURITES_FILE, "w") as file:
        json.dump(data, file, indent=4)


def fuel(distance, fuel_price, mileage):

    fuel_required = distance / mileage
    trip_cost = fuel_required * fuel_price

    return round(fuel_required, 2), round(trip_cost, 2)

def statistics():
    history = load_history()

    total_trips = len(history)

    if total_trips == 0:
        return {
            "total_trips": 0,
            "total_distance": 0,
            "average_time": 0,
            "total_cost": 0,
            "most_visited": "N/A",
            "common_source": None
        }
    
    total_distance = sum(trip["distance"] for trip in history)
    avg_time = (sum( trip["estimated_travel_time"] for trip in history) / total_trips)
    total_cost = sum(trip["trip_cost"] for trip in history)

    destination_count = {}
    source_count = {}

    for trip in history:
        destination = trip["destination"]
        source = trip["source"]

        if destination in destination_count:
            destination_count[destination] += 1
        else:
            destination_count[destination] = 1

        if source in source_count:
            source_count[source] += 1
        else:
            source_count[source] = 1

    most_common_destination = max(destination_count,key=destination_count.get,default="N/A")
    most_common_source = max(source_count,key=source_count.get,default="N/A")

    return {
        "total_trips" : total_trips,
        "total_distance" : total_distance,
        "average_time" : avg_time,
        "total_cost" : total_cost,
        "most_visited" : most_common_destination,
        "common_source" : most_common_source
    }