# 🌾 Kishan Saathi AI

> **“Har Kisan Ka Smart Digital Saathi”**  
An AI-powered smart agriculture assistant built to help farmers with crop guidance, weather forecasting, plant disease detection, government schemes, soil recommendations, and multilingual AI support.

---

# 📌 Project Overview

## 🚜 About the Project

**Kishan Saathi AI** is an intelligent agriculture support platform designed for farmers and rural communities.  
The goal of this project is to make modern AI technology accessible to every farmer through a simple and user-friendly web platform.

This platform combines:

- 🌦 Weather Intelligence
- 🌱 Crop Recommendation
- 🦠 Disease Detection
- 🏛 Government Scheme Assistance
- 🌍 Multi-language Support
- 🤖 AI Chatbot Guidance

All inside one unified agricultural ecosystem.

The platform is developed using **Flask**, **Machine Learning**, **MongoDB**, and modern frontend technologies.

---

# ✨ Features

## 🌾 Smart Crop Recommendation
- Suggests suitable crops based on:
  - Soil type
  - Weather
  - Temperature
  - Humidity
  - Rainfall

---

## 🦠 Plant Disease Detection
- Upload crop images
- AI predicts disease
- Provides prevention suggestions

---

## 🌦 Live Weather Dashboard
- Real-time weather updates
- Temperature conversion (°C ↔ °F)
- Humidity
- Wind speed
- Sunrise & sunset data

---

## 🏛 Government Scheme Assistant
- Fetches farmer-related schemes
- Insurance support information
- Agriculture subsidy guidance

---

## 🤖 AI Farming Assistant Chatbot
- Interactive AI chatbot
- Answers farming questions
- Provides agricultural guidance
- Supports multilingual conversations

---

## 🌍 Multi-language Support
Designed for accessibility for Indian farmers.

Possible supported languages:
- Hindi
- English
- Regional languages

---

## 🔐 Authentication System
- Farmer Login/Register
- Admin Panel
- Session Management
- MongoDB-based authentication

---

## 👨‍💼 Admin Dashboard
Admin can:
- Manage users
- Monitor platform usage
- Handle agricultural data
- Manage uploaded files

---

# 🛠 Tech Stack

## Backend
- Python
- Flask
- Flask Blueprints
- REST APIs

## Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

## Database
- MongoDB

## AI / ML
- Scikit-learn
- Machine Learning Models
- Image Prediction Models

## APIs & Services
- Weather APIs
- Translation APIs
- AI Chat APIs

---

# 📂 Project Structure

```bash
KISHAN-SAATHI-AI/
│
├── auth/                    # Authentication & Authorization System
│   ├── routes.py            # Login/Register Routes
│   ├── models.py            # User Models
│   └── utils.py             # Password & Session Utilities
│
├── data/                    # Datasets & CSV Files
│   ├── crop_data.csv
│   ├── soil_data.csv
│   └── disease_data.csv
│
├── ml/                      # Machine Learning Models & Prediction Logic
│   ├── crop_prediction.py
│   ├── disease_prediction.py
│   ├── soil_prediction.py
│   └── trained_models/
│
├── routes/                  # Flask Application Routes
│   ├── chat.py              # AI Chatbot Routes
│   ├── crop_routes.py       # Crop Recommendation Routes
│   ├── disease_routes.py    # Disease Detection Routes
│   ├── greet.py             # Greeting & Intro Routes
│   ├── language.py          # Language Translation Routes
│   ├── tts.py               # Text-to-Speech Routes
│   └── weather_routes.py    # Weather Dashboard Routes
│
├── services/                # Backend Business Logic & APIs
│   ├── scraper.py           # Government Scheme Scraper
│   ├── stt_service.py       # Speech-to-Text Service
│   ├── translate_service.py # Translation Service
│   ├── weather_service.py   # Weather API Service
│   └── chatbot_service.py   # AI Chatbot Logic
│
├── static/                  # Static Assets
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript Files
│   ├── images/              # Images & Icons
│   └── videos/              # Media Files
│
├── templates/               # HTML Templates
│   ├── admin.html           # Admin Dashboard
│   ├── chat.html            # AI Chat Interface
│   ├── disease.html         # Disease Detection Page
│   ├── govtscheme.html      # Government Schemes Page
│   ├── home.html            # Home Page
│   ├── result.html          # Prediction Results Page
│   ├── signin.html          # Login Page
│   ├── signup.html          # Registration Page
│   ├── soil.html            # Soil Analysis Page
│   └── weather.html         # Weather Dashboard
│
├── .env                     # Environment Variables
├── app.py                   # Main Flask Application
├── config.py                # Project Configuration
├── extensions.py            # Flask Extensions Initialization
├── requirements.txt         # Python Dependencies
└── README.md                # Project Documentation
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Adi-ADI2005/kishan-saathi-ai.git

cd kishan-saathi-ai
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

### Windows
```bash
venv\Scripts\activate
```

### Linux / Mac
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Setup Environment Variables

Create a `.env` file:

```env
SARVAM_API_KEY=your_api_key
OPENROUTER_API_KEY=your_api_key
WEATHER_API_KEY=2your_api_key
MONGO_URI=your_mongodb_url
SECRET_KEY=your_secret_key
---

## 5️⃣ Run the Application

```bash
python app.py
```

---

# 🎯 Future Enhancements

- 📱 Mobile Application
- 🛰 Satellite-based Crop Monitoring
- 📊 Farmer Analytics Dashboard
- 🎙 Voice Assistant Support
- 🌐 Regional Language Expansion
- 🤝 Marketplace for Farmers

---

# 👨‍💻 Developed By

## Aditya Mishra

Passionate about:
- Artificial Intelligence
- Macchine Leaning
- Deep Learning 
- Full Stack Development


---

# ❤️ Vision

The vision of **Kishan Saathi AI** is to empower farmers with AI-driven technology and make smart agriculture accessible, affordable, and easy to use for everyone.

---

# 📜 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you like this project:
- Give it a ⭐ on GitHub
- Share it with others
- Support smart farming innovation 🌱
