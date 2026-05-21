import requests
from flask import Response
from config import SARVAM_API_KEY, BASE_URL

def generate_tts_stream(text, lang_code):
    url = f"{BASE_URL}/text-to-speech/stream"

    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "target_language_code": lang_code,
        "speaker": "ritu",
        "model": "bulbul:v3",
        "pace": 1.1,
        "speech_sample_rate": 22050,
        "output_audio_codec": "mp3",
        "enable_preprocessing": True
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)

    # ✅ Error handling
    if response.status_code != 200:
        return Response("TTS API Error", status=500)

    # ✅ Direct streaming (NO file saving)
    return Response(
        response.iter_content(chunk_size=1024),
        content_type="audio/mpeg"
    )