from sarvamai import SarvamAI
from config import SARVAM_API_KEY
import re

client = SarvamAI(api_subscription_key=SARVAM_API_KEY)


def translate_text(text, source_lang, target_lang):
    try:
        if source_lang == target_lang:
            return text

        # ✅ Strong placeholder
        placeholder = "<<<AGROAI>>>"
        text = re.sub(r"AgroAI", placeholder, text, flags=re.IGNORECASE)

        response = client.text.translate(
            input=text,
            source_language_code=source_lang,
            target_language_code=target_lang,
            model="mayura:v1"
        )

        translated = response.translated_text

        # ✅ Restore AgroAI
        translated = re.sub(r"<+\s*AGROAI\s*>+", "AgroAI", translated, flags=re.IGNORECASE)

        # 🚨 FIX: Remove wrong conversions like agroai.com
        translated = re.sub(r"agroai\.com", "AgroAI", translated, flags=re.IGNORECASE)

        # 🚨 FIX: Remove unwanted "website" words (Odia + English)
        translated = re.sub(r"\b(website|ୱେବସାଇଟ)\b", "", translated, flags=re.IGNORECASE)

        # ✅ Clean extra spaces
        translated = re.sub(r"\s+", " ", translated).strip()

        return translated

    except Exception as e:
        print("Translation error:", e)
        return text