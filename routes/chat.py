from flask import Blueprint, request, jsonify
import os
import requests
from extensions import csrf
from services.translate_service import translate_text
from services.stt_service import speech_to_text
from services.scraper import get_schemes

from routes.greet import get_intro_greeting
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL

chat_bp = Blueprint("chat", __name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ==========================
# 🌱 AGRICULTURE DETECTION
# ==========================
def is_agriculture_query(text):
    text = text.lower()

    keywords = [
        "crop", "rice", "wheat", "paddy", "farming", "farm",
        "soil", "fertilizer", "pesticide", "irrigation",
        "seed", "harvest", "agriculture", "mandi",
        "disease", "plant", "weather", "farmer",
        "livestock", "cow", "goat", "tractor",
        "sowing", "cultivation", "field",
        "rabi", "kharif", "zaid", "winter"
    ]

    return any(word in text for word in keywords)


# ==========================
# 🤖 AI RESPONSE
# ==========================
def generate_agro_response(text):
    try:
        url = f"{OPENROUTER_BASE_URL}/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an agriculture expert. Give short, practical answers."
                },
                {"role": "user", "content": text}
            ],
            "temperature": 0.6
        }

        res = requests.post(url, headers=headers, json=payload, timeout=15)
        data = res.json()

        if res.status_code == 200:
            return data["choices"][0]["message"]["content"]

        return "AI service error."

    except Exception as e:
        print("AI ERROR:", e)
        return "AI is temporarily unavailable."


# ==========================
# 🏛 SCHEME + INSURANCE LOGIC
# ==========================
def scheme_response(text):
    text_lower = text.lower()

    schemes = get_schemes()

    # ✅ Fallback (VERY IMPORTANT)
    if not schemes:
        schemes = [
            {
                "name": "PMFBY (Crop Insurance)",
                "description": "Provides insurance coverage for crop loss due to natural disasters."
            },
            {
                "name": "PM-KISAN",
                "description": "₹6000 yearly financial support for farmers."
            },
            {
                "name": "KCC (Kisan Credit Card)",
                "description": "Low-interest loans for farming needs."
            }
        ]

    # ======================
    # 🏛 SCHEMES
    # ======================
    if any(word in text_lower for word in ["scheme", "yojana"]):
        reply = "📄 Government Schemes:\n\n"

        for s in schemes[:3]:
            reply += f"🏛️ {s['name']}\n"
            reply += f"👉 {s['description']}\n\n"

        reply += "💡 Ask: insurance or claim process"
        return reply

    # ======================
    # 🛡 INSURANCE
    # ======================
    if any(word in text_lower for word in ["insurance", "bima"]):
        reply = "🛡️ Crop Insurance Schemes:\n\n"

        for s in schemes[:2]:
            reply += f"📌 {s['name']}\n"
            reply += f"👉 {s['description']}\n\n"

        reply += "💡 Type 'claim insurance' to know process"
        return reply

    # ======================
    # 🧾 CLAIM PROCESS
    # ======================
    if "claim" in text_lower:
        return """🛡️ Insurance Claim Process (PMFBY)

1️⃣ Inform within 72 hours of crop damage  
2️⃣ Visit nearest bank / agriculture office  
3️⃣ Submit:
   - Aadhaar Card  
   - Land documents  
   - Crop details  
4️⃣ Field inspection  
5️⃣ Compensation sent to bank  

🌾 This protects farmers from losses"""

    return None


# ==========================
# 👋 GREETING
# ==========================
def process_query_english(text, user_lang):
    text_lower = text.lower().strip()

    greetings = [
        "hi", "hello", "hey", "namaste",
        "good morning", "good evening"
    ]

    if text_lower in greetings:
        return get_intro_greeting(user_lang)

    return None


# ==========================
# 💬 MAIN CHAT ROUTE
# ==========================
@chat_bp.route("", methods=["POST"])
@csrf.exempt   # ✅ ADD THIS
def chat():
    try:
        data = request.get_json(silent=True) or {}
        user_lang = data.get("language", "en-IN")

        # ======================
        # 🎤 VOICE INPUT
        # ======================
        if "audio" in request.files:
            audio = request.files["audio"]
            path = os.path.join(UPLOAD_FOLDER, audio.filename)
            audio.save(path)
            user_text = speech_to_text(path)
        else:
            user_text = data.get("message")

        if not user_text:
            return jsonify({"response": "No input"}), 400

        # ======================
        # 🌍 TRANSLATE
        # ======================
        text_en = translate_text(user_text, "auto", "en-IN")

        print("USER:", text_en)

        # ======================
        # 1️⃣ GREETING
        # ======================
        res = process_query_english(text_en, user_lang)

        # ======================
        # 2️⃣ SCHEME / INSURANCE
        # ======================
        if not res:
            res = scheme_response(text_en)

        # ======================
        # 3️⃣ AI AGRICULTURE
        # ======================
        if not res and is_agriculture_query(text_en):
            ai = generate_agro_response(text_en)
            res = translate_text(ai, "en-IN", user_lang)

        # ======================
        # 4️⃣ DEFAULT
        # ======================
        if not res:
            res = translate_text(
                "I can help with crops, schemes, and insurance.",
                "en-IN",
                user_lang
            )

        return jsonify({
            "response": res
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "response": "⚠️ Server error. Try again."
        }), 500