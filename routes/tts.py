from flask import Blueprint, request
from services.tts_service import generate_tts_stream
from extensions import csrf
tts_bp = Blueprint("tts", __name__)

@tts_bp.route("/", methods=["POST"])   # ✅ IMPORTANT
@csrf.exempt   
def tts():
    print("✅ TTS ROUTE HIT")  # debug

    data = request.get_json(silent=True) or {}

    text = data.get("text")
    lang = data.get("language", "en-IN")

    if not text:
        return {"error": "No text provided"}, 400

    return generate_tts_stream(text, lang)