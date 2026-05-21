import requests
from datetime import datetime
from config import WEATHER_API_KEY, WEATHER_BASE_URL, KELVIN

# 🌤️ ICON FILTER
def weather_icon(desc):
    if not desc:
        return "🌡️"
    d = desc.lower()
    if "cloud" in d: return "☁️"
    if "rain" in d: return "🌧️"
    if "clear" in d: return "☀️"
    if "storm" in d: return "⛈️"
    if "snow" in d: return "❄️"
    if "mist" in d or "fog" in d: return "🌫️"
    return "🌤️"


def format_time(ts, tz):
    return datetime.utcfromtimestamp(ts + tz).strftime("%H:%M")


def format_day_time(ts, tz):
    return datetime.utcfromtimestamp(ts + tz).strftime("%a %H:%M")


def get_weather(city=None, lat=None, lon=None):
    try:
        if lat and lon:
            loc = f"lat={lat}&lon={lon}"
        elif city:
            loc = f"q={city}"
        else:
            return {}, [], [], "No location"

        weather_url = f"{WEATHER_BASE_URL}/weather?{loc}&appid={WEATHER_API_KEY}"
        forecast_url = f"{WEATHER_BASE_URL}/forecast?{loc}&appid={WEATHER_API_KEY}"

        w = requests.get(weather_url).json()

        if w.get("cod") != 200:
            return {}, [], [], "City not found"

        tz = w["timezone"]
        coord = w["coord"]

        f = requests.get(forecast_url).json()

        # Hourly
        hourly = []
        for item in f["list"][:12]:
            hourly.append({
                "datetime": format_day_time(item["dt"], tz),
                "temperature": int(item["main"]["temp"] - KELVIN),
                "description": item["weather"][0]["description"]
            })

        # Daily
        daily = []
        seen = set()

        for item in f["list"]:
            date = item["dt_txt"].split(" ")[0]
            if date not in seen and "12:00:00" in item["dt_txt"]:
                seen.add(date)
                daily.append({
                    "date": date,
                    "datetime": format_day_time(item["dt"], tz),
                    "temperature": int(item["main"]["temp"] - KELVIN),
                    "description": item["weather"][0]["description"]
                })
            if len(daily) == 5:
                break

        weather = {
            "city": w["name"],
            "temperature": int(w["main"]["temp"] - KELVIN),
            "feels_like": int(w["main"]["feels_like"] - KELVIN),
            "humidity": w["main"]["humidity"],
            "pressure": w["main"]["pressure"],
            "cloudiness": w["clouds"]["all"],
            "description": w["weather"][0]["description"],
            "visibility": round(w.get("visibility", 10000)/1000, 1),
            "sunrise": format_time(w["sys"]["sunrise"], tz),
            "sunset": format_time(w["sys"]["sunset"], tz),
            "wind_speed": w["wind"]["speed"],
            "wind_direction": w["wind"].get("deg", 0),
            "aqi": "N/A",
            "sea_level": w["main"].get("sea_level", "N/A"),
            "grnd_level": w["main"].get("grnd_level", "N/A"),
        }

        return weather, hourly, daily, None

    except Exception as e:
        print(e)
        return {}, [], [], "Error fetching weather"