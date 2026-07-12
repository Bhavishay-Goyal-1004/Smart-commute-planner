# 🚗 Smart Commute Planner
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-Web_App-black)
![Deployment](https://img.shields.io/badge/Deployment-Railway-purple)

![Google_GenAI](https://img.shields.io/badge/Google_GenAI-Gemini-orange)
![OpenRouteService](https://img.shields.io/badge/OpenRouteService-Routing-success)
![TomTom_API](https://img.shields.io/badge/TomTom-Traffic-red)
![OpenWeather_API](https://img.shields.io/badge/OpenWeather-Weather-blue)


An AI-powered Smart Commute Planner built using Flask that helps users plan efficient daily travel by combining route information, live traffic, weather conditions, and AI-generated travel recommendations.

The application calculates the best route between two locations, displays distance and estimated travel time, checks current weather conditions, provides live traffic information, and generates personalized travel advice using Google's Gemini AI.

---

## 🌐 Live Demo
 
[Visit Live Website](https://commute-planner.up.railway.app/)

---

## 📌 Features

- 📍 Calculate route between source and destination
- 🛣️ Distance and travel time using OpenRouteService API
- 🚦 Live traffic updates using TomTom Traffic API
- 🌤️ Real-time weather information using OpenWeather API
- 🤖 AI-powered commute recommendations using Google Gemini
- ⭐ Save favourite routes
- 🕒 View commute history
- 📊 Dashboard with previous trips
- 💻 Clean and responsive user interface

---

## 🛠 Tech Stack

### Frontend
- HTML5
- CSS3
- Jinja2 Templates

### Backend
- Python
- Flask

### APIs
- OpenRouteService API
- TomTom Traffic API
- OpenWeather API
- Google Gemini API

### Storage
- JSON Files

---

## 📂 Project Structure

```text
Smart-Commute-Planner/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
│
├── services/
│   ├── weather_service.py
│   ├── route_service.py
│   ├── traffic_service.py
│   ├── ai_service.py
│   ├── history_service.py
│   └── favourite_service.py
│
├── templates/
├── static/
├── data/
│   ├── history.json
│   └── favourites.json
└── README.md
```

---

# ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Smart-Commute-Planner.git
```

### 2. Move into the project folder

```bash
cd Smart-Commute-Planner
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
OPENWEATHER_API_KEY=your_api_key
OPENROUTESERVICE_API_KEY=your_api_key
TOMTOM_API_KEY=your_api_key
GEMINI_API_KEY=your_api_key
```

### 5. Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# 📸 Screenshots

## Home Page

<img width="1920" height="971" alt="image" src="https://github.com/user-attachments/assets/b35e804a-298b-4fc2-a77f-413329f7038f" />

## Result Page

<img width="1920" height="977" alt="image" src="https://github.com/user-attachments/assets/46d03442-844c-4ddb-8877-cf38da793c5a" />

## Dashboard

<img width="1920" height="977" alt="{3F2B166D-17EA-463C-9232-6384497E6B59}" src="https://github.com/user-attachments/assets/110fbb88-82ae-4dc2-ac86-94ab09bd66bc" />

---

# 📦 Requirements

Install all dependencies using:

```bash
pip install -r requirements.txt
```

Main packages used:

- Flask
- requests
- python-dotenv
- google-genai

---

# 🔮 Future Improvements

- User authentication
- Multiple route comparison
- Interactive maps
- Public transport integration
- Carbon footprint calculator
- Database integration
- Improved mobile responsiveness

---

# 🧠 Reflection

Building the Smart Commute Planner was one of the most practical projects I have worked on because it required integrating multiple APIs into a single application. The most challenging part was combining data from different services, including route calculation, weather updates, traffic information, and AI-generated travel recommendations. Each API returned data in a different format, so understanding the response structures and handling errors consistently required careful debugging.

Another challenge was ensuring that the application continued to work even when an API failed or returned incomplete data. Implementing proper exception handling and validating user input helped improve the overall reliability of the application. Managing project structure by separating logic into different service files also made the project easier to maintain and understand.

If I had more time, I would improve the project by adding user authentication, storing history in a database instead of JSON files, integrating interactive maps, comparing multiple routes, and calculating estimated carbon emissions. These additions would make the application more useful for daily commuters.

This project significantly improved my understanding of Flask application development, REST API integration, JSON data handling, environment variables, and organizing code into reusable modules. I also became more confident in debugging API responses, structuring larger Python projects, and designing a web application that combines multiple external services into one user-friendly interface.

---

# 👨‍💻 Author

**Bhavishay Goyal**
