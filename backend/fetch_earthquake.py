import requests
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["disaster_management"]

def fetch_usgs_earthquakes():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    r = requests.get(url)
    eqs = r.json()["features"]
    for eq in eqs:
        props = eq["properties"]
        coords = eq["geometry"]["coordinates"]  # [lon, lat, depth]
        incident = {
            "title": props["place"],
            "description": f"Magnitude {props['mag']} at depth {coords[2]}km",
            "disaster_type": "earthquake",
            "severity": int(min(max(props["mag"] or 1, 1), 5)),  # scale 1-5
            "latitude": coords[1],
            "longitude": coords[0],
            "status": "active",
            "reported_by": "USGS",
            "created_at": datetime.utcfromtimestamp(props["time"]/1000),
        }
        # Avoid duplicates by unique place+created_at
        if not db.incidents.find_one({"title":props["place"], "created_at":incident["created_at"]}):
            db.incidents.insert_one(incident)
    print("Earthquake data ingested.")

if __name__ == "__main__":
    fetch_usgs_earthquakes()
