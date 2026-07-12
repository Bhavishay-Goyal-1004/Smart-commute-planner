from flask import Flask, render_template, request, redirect
import json
from services.utils import *
from services.ai_service import *
from services.route_service import *
from services.traffic_service import *
from services.weather_service import *
from datetime import datetime
import traceback


app = Flask(__name__)

def generate_trip(source,destination,vehicle_mileage,fuel_price):
    now = datetime.now()

    try:

        route = get_route(source,destination)
        print("ROUTE DATA:",route)
        distance = route['distance']
        travel_time = route['travel_time']
        start_coord = route['start']
        end_coord = route['end']

        traffic = get_traffic(start_coord,end_coord)

        peak_hour = get_peak_hour(traffic["congestion"])

        weather_data = get_weather(destination,end_coord)

        fuel_data = fuel(distance,fuel_price,vehicle_mileage)
        fuel_required = fuel_data[0]
        trip_cost = fuel_data[1]

        ai_advice = get_info(
            source,
            destination,
            weather_data,
            distance,
            trip_cost,
            traffic,
            travel_time
        )

        data = {
        "source": source,
        "destination": destination,
        "distance": distance,
        "estimated_travel_time": travel_time,
        "traffic_travel_time": traffic['traffic_time'],
        "delay": traffic['delay'],
        "congestion": traffic['congestion'],
        "peak_hour" : peak_hour,
        "weather": f"{weather_data['condition']}, {weather_data['temperature']}°C",
        "trip_cost": trip_cost,
        "ai_advice": ai_advice,
        "date": now.strftime("%d-%m-%Y"),
        "time": now.strftime("%I:%M %p")
        }
        
        history = load_history()
        history.append(data)

        if len(history) > 100:
            history = history[-100:]

        save_history(history)

        return render_template(
        "result.html",
        source=source,
        destination=destination,
        distance=distance,
        travel_time=travel_time,
        traffic=traffic,
        peak_hour=peak_hour,
        weather=weather_data,
        vehicle_mileage=vehicle_mileage,
        fuel_price=fuel_price,
        fuel_required=fuel_required,
        trip_cost=trip_cost,
        ai_advice=ai_advice
        )


    except Exception as e:
        traceback.print_exc()

        return render_template(
            "index.html",
            error=str(e)
        )

@app.route("/")
def home():
    
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    
    stats = statistics()

    weather = None

    if stats["common_source"]:
        try:
            weather = get_weather(stats["common_source"])
        except Exception:
            weather = None

    history = load_history()
    recent_trips = history[-5:][::-1]
    
    ai_tip = None

    if history:
        latest_trip = history[-1]

        if "ai_advice" in latest_trip:
            advice = latest_trip["ai_advice"]

            if isinstance(advice, dict):
                if "tips" in advice and advice["tips"]:
                    ai_tip = advice["tips"][0]
                elif "summary" in advice:
                    ai_tip = advice["summary"]

    return render_template(
        "dashboard.html",
        weather=weather,
        stats=stats,
        recent_trips=recent_trips,
        ai_tip=ai_tip
    )

@app.route("/plan", methods=["POST"])
def plan_journey():

    source = request.form.get("source")
    destination = request.form.get("destination")
    vehicle_mileage = request.form.get("mileage")
    fuel_price = request.form.get("fuel_price")
    
    fields = {
    "Source": source,
    "Destination": destination,
    "Mileage": vehicle_mileage,
    "Fuel Price": fuel_price
    }

    for name, value in fields.items():
        if not value or value.strip() == "":
            return render_template(
                "index.html",
                error=f"Please enter {name}."
            )
    
    if source == destination:
        return render_template(
                "index.html",
                error=f"Source & Destination cannot be same."
            )

        
    try:
        vehicle_mileage = float(vehicle_mileage)
        fuel_price = float(fuel_price)
    
    except ValueError:
        return render_template(
            "index.html",
            error="Mileage and Fuel Price must be valid numbers."
        )

    if source.strip().lower() == destination.strip().lower():
        return render_template(
            "index.html",
            error="Source and Destination cannot be the same."
        )
            
    return generate_trip(source,destination,vehicle_mileage,fuel_price)

@app.route("/history")
def history():
    history = load_history()

    return render_template(
        "history.html",
        history=history
    )

@app.route("/repeat-history", methods=["POST"])
def repeat_history():

    source = request.form.get("source")
    destination = request.form.get("destination")
    vehicle_mileage = request.form.get("mileage")
    fuel_price = request.form.get("fuel_price")

    try:
        vehicle_mileage = float(vehicle_mileage)
        fuel_price = float(fuel_price)
    
    except ValueError:
        return render_template(
            "index.html",
            error="Mileage and Fuel Price must be valid numbers."
        )

    if source.strip().lower() == destination.strip().lower():
        return render_template(
            "index.html",
            error="Source and Destination cannot be the same."
        )
    
    return generate_trip(source,destination,vehicle_mileage,fuel_price)

@app.route("/delete-history", methods=["POST"])
def delete_history():
    
    index = int(request.form.get("index"))

    history = load_history()
    history.pop(index)
    save_history(history)

    return redirect("/history")

@app.route("/favourites")
def favourites():
    favourites = load_favourites()

    return render_template(
        "favourites.html",
        favourites=favourites
    )

@app.route("/add-favourite", methods=["POST"])
def add_favourites():
    source = request.form.get("source")
    destination = request.form.get("destination")

    favourites = load_favourites()

    favourite_route = {
        "name": f"{source} → {destination}",
        "source": source,
        "destination": destination
    }

    already_exists = False

    for route in favourites:
        if (route["source"].lower() == source.lower() and
            route["destination"].lower() == destination.lower()):
            already_exists = True
            break

    if not already_exists:
        favourites.append(favourite_route)
        save_favourites(favourites)

    return redirect("/favourites")

@app.route("/repeat-favourites", methods=["POST"])
def repeat_favourites():

    source = request.form.get("source")
    destination = request.form.get("destination")
    vehicle_mileage = request.form.get("mileage")
    fuel_price = request.form.get("fuel_price")

    try:
        vehicle_mileage = float(vehicle_mileage)
        fuel_price = float(fuel_price)
    
    except ValueError:
        return render_template(
            "index.html",
            error="Mileage and Fuel Price must be valid numbers."
        )

    if source.strip().lower() == destination.strip().lower():
        return render_template(
            "index.html",
            error="Source and Destination cannot be the same."
        )

    return generate_trip(source,destination,vehicle_mileage,fuel_price)

@app.route("/remove-favourite", methods=["POST"])
def remove_favourite():
    index = int(request.form.get("index"))

    favourites = load_favourites()
    favourites.pop(index)
    save_favourites(favourites)

    return redirect("/favourites")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)