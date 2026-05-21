from flask import Flask, render_template, session, redirect, url_for, jsonify
from flask_wtf import CSRFProtect
from extensions import csrf

# Blueprints
from routes.chat import chat_bp
from routes.greet import greet_bp
from routes.language import lang_bp
from routes.tts import tts_bp
from routes.crop_routes import crop_bp
from routes.weather_routes import weather_bp
from auth.routes import auth_bp   
from routes.disease_routes import disease_bp
from routes.scheme_routes import scheme_bp

# Services
from services.weather_service import weather_icon
from services.scraper import get_schemes

app = Flask(__name__)
app.secret_key = "agriculture_secret_key_123"

csrf.init_app(app)
@app.before_request
def test_csrf():
    print("CSRF ENABLED:", app.config.get("WTF_CSRF_ENABLED"))
# ==========================
# REGISTER BLUEPRINTS
# ==========================
app.register_blueprint(auth_bp)  # ✅ AUTH handles / and /signup

app.register_blueprint(chat_bp, url_prefix="/chat")
app.register_blueprint(greet_bp, url_prefix="/greet")
app.register_blueprint(lang_bp, url_prefix="/lang")
app.register_blueprint(tts_bp, url_prefix="/tts")
app.register_blueprint(crop_bp, url_prefix="/crop")
app.register_blueprint(weather_bp, url_prefix="/weather")
app.register_blueprint(disease_bp)
app.register_blueprint(scheme_bp)
# Jinja filter
app.jinja_env.filters["weather_icon"] = weather_icon

# ==========================
# PROTECTED ROUTES
# ==========================

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("auth.signin"))
    return render_template(
        "home.html",
        first_name=session.get("first_name")
    )


@app.route("/admin")
def admin():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.signin"))
    return render_template("admin.html",first_name=session.get("first_name"))


@app.route("/chatbot")
def chatbot_page():
    if "user" not in session:
        return redirect(url_for("auth.signin"))
    return render_template("chat.html")


@app.route("/crop-page")
def crop_page():
    if "user" not in session:
        return redirect(url_for("auth.signin"))
    return render_template("soil.html")

@app.route("/weather")
def weather():
    if "user" not in session:
        return redirect(url_for("auth.signin"))
    return render_template("weather.html")


@app.route("/disease")
def disease():
    if "user" not in session:
        return redirect(url_for("auth.signin"))
    return render_template("disease.html")


@app.route("/govt_scheme")
def govt_scheme():
    if "user" not in session:
        return redirect(url_for("auth.signin"))
    return render_template("govtscheme.html")


@app.route("/api/schemes")
def schemes_api():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(get_schemes())


# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    app.run()
    
