import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

CACHE_FILE = "data/schemes_cache.json"


# ==============================
# 🔍 CLEAN TEXT HELPER
# ==============================
def clean_text(text):
    return " ".join(text.split()).strip()


# ==============================
# 🌾 SCRAPE STRUCTURED DATA
# ==============================
def scrape_pmfby():
    url = "https://pmfby.gov.in"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        schemes = []

        # 🔹 Find content blocks
        sections = soup.find_all(["section", "div"])

        for sec in sections:
            title_tag = sec.find(["h1", "h2", "h3"])
            para_tags = sec.find_all("p")

            if not title_tag or not para_tags:
                continue

            title = clean_text(title_tag.get_text())
            description = clean_text(para_tags[0].get_text())

            # 🔹 Extract benefits (if list exists)
            benefits = []
            ul = sec.find("ul")
            if ul:
                for li in ul.find_all("li"):
                    benefits.append(clean_text(li.get_text()))

            # 🔹 Filter relevant content
            keywords = ["insurance", "crop", "farmer", "scheme"]
            if not any(k in title.lower() for k in keywords):
                continue

            schemes.append({
                "name": title,
                "description": description,
                "benefits": benefits,
                "source": url
            })

        return schemes

    except Exception as e:
        print("Scraping error:", e)
        return []
# 4️⃣ ✅ SMART CACHE SYSTEM (PLACE HERE)
def save_cache(data):
    os.makedirs("data", exist_ok=True)

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "last_updated": datetime.now().isoformat(),
            "data": data
        }, f, indent=4)


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_schemes():
    cache = load_cache()

    if cache:
        last_updated = datetime.fromisoformat(cache["last_updated"])
        if (datetime.now() - last_updated).seconds < 21600:
            return cache["data"]

    data = scrape_pmfby()

    if data:
        save_cache(data)

    return data