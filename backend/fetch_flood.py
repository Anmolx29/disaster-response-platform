import requests
from pymongo import MongoClient
from datetime import datetime

API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
LOC = {"lat": 28.61, "lon": 77.20}  # Example: Delhi coordinates

client = MongoClient("mongodb://localhost:27017")
db = client["disaster_management"]

def fetch_openweather_flood():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LOC['lat']}&lon={LOC['lon']}&appid={API_KEY}&units=metric"
    r = requests.get(url)
    data = r.json()
    rainfall = data.get('rain', {}).get('1h', 0)
    # Insert if threshold exceeded (demo: >30mm means flood)
    if rainfall > 30:
        incident = {
            "title": f"Heavy Rain in {data['name']}",
            "description": f"{rainfall:.1f}mm rainfall in 1hr detected.",
            "disaster_type": "flood",
            "severity": 5 if rainfall > 60 else 3,
            "latitude": LOC["lat"],
            "longitude": LOC["lon"],
            "status": "active",
            "reported_by": "OpenWeatherMap",
            "created_at": datetime.utcnow()
        }
        db.incidents.insert_one(incident)
        print("Flood incident inserted.")
    else:
        print("No flood detected.")

if __name__ == "__main__":
    fetch_openweather_flood()
