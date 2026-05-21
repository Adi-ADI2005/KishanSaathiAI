import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()

# ==========================
# SARVAM AI (TTS + STT + Translation)
# ==========================
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
BASE_URL = "https://api.sarvam.ai"

# ==========================
# OPENROUTER (LLM / CHAT AI)
# ==========================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

print("OPENROUTER KEY LOADED:", OPENROUTER_API_KEY is not None)

# ==========================
# weather API
# ==========================
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY") 
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5" 
KELVIN = 273.15 
print("WEATHER API KEY LOADED:", WEATHER_API_KEY is not None)

#===========================
# MONGODB DATABASE
#===========================

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["agroai_db"]

users_collection = db["users"]

schemes_collection = db["schemes"]