from flask import Blueprint, request, jsonify
from datetime import datetime
from services.translate_service import translate_text

greet_bp = Blueprint("greet", __name__)


# 🔥 1. APP LOAD GREETING (time-based)
def get_time_greeting(user_lang="en-IN"):
    hour = datetime.now().hour

    if 5 <= hour < 12:
        text = "Good Morning!"
    elif 12 <= hour < 17:
        text = "Good Afternoon!"
    elif 17 <= hour < 21:
        text = "Good Evening!"
    else:
        text = "Good Night!"

    text = f"{text} Welcome to AgroAI!"

    return translate_text(text, "en-IN", user_lang)


# 🔥 2. HI GREETING (assistant intro)
def get_intro_greeting(user_lang="en-IN"):
    text = "Hello! Today I am your AI assistant. How can I help you today?"

    return translate_text(text, "en-IN", user_lang)


# 🌐 API ROUTE (used on page load)
@greet_bp.route("/greet", methods=["GET"])
def greet():
    user_lang = request.args.get("lang", "en-IN")

    return jsonify({
        "message": get_time_greeting(user_lang)
    })