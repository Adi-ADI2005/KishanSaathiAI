from flask import Blueprint, jsonify

lang_bp = Blueprint("language", __name__)

@lang_bp.route("/languages", methods=["GET"])
def language():
    return jsonify({
        "English": "en-IN",
        "Hindi": "hi-IN",
        "Odia": "od-IN",
        "Bengali": "bn-IN",
        "Gujarati": "gu-IN",
        "Kannada": "kn-IN",
        "Malayalam": "ml-IN",
        "Marathi": "mr-IN",
        "Punjabi": "pa-IN",
        "Tamil": "ta-IN",
        "Telugu": "te-IN"
    })