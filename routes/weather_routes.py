from flask import Blueprint, render_template, request
from services.weather_service import get_weather
from datetime import datetime

weather_bp = Blueprint("weather", __name__, url_prefix="/weather")


# ✅ Home page (initial load)
@weather_bp.route("/", methods=["GET"])
def home():
    return render_template(
        "weather.html",
        weather=None,
        hourly=None,
        weekly=None,
        error=None,
        date=datetime.now().strftime("%d %B %Y"),
    )


# ✅ Weather fetch using GET (city OR lat/lon)
@weather_bp.route("", methods=["GET"])
def weather_home():
    weather_data = None
    hourly_data = None
    daily_data = None
    error_msg = None
    current_date = datetime.now().strftime("%d %B %Y")

    # Get query params
    city = request.args.get("city")
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    # Convert lat/lon safely
    try:
        lat = float(lat) if lat else None
        lon = float(lon) if lon else None
    except:
        lat = lon = None

    # ✅ Fetch weather
    if city:
        weather_data, hourly_data, daily_data, error_msg = get_weather(city=city)

    elif lat is not None and lon is not None:
        weather_data, hourly_data, daily_data, error_msg = get_weather(lat=lat, lon=lon)

    else:
        error_msg = "Enter city or allow location."

    return render_template(
        "weather.html",
        weather=weather_data,
        hourly=hourly_data,
        weekly=daily_data,
        error=error_msg,
        date=current_date,
    )