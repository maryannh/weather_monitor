from pymongo import MongoClient
import requests
import dns
import schedule
import time
from datetime import datetime, timedelta

import config

client = MongoClient(config.MONGO_URI)
db = client.news

def flood_warnings():
    payload = {"lat": config.LAT, "long": config.LONG, "dist": 1}
    r = requests.get(config.FLOOD_API_URL, params=payload)
    data = r.json()
    warning = data["items"][0]["severityLevel"]
    return warning

def update_weather():
    info = {
        "flood_warning": flood_warnings(),
        "date_added": datetime.utcnow(),
    }
    _id = db.weather.insert_one(info)

schedule.every().day.at("05:30").do(update_weather)

while True:
    schedule.run_pending()
    time.sleep(1)
