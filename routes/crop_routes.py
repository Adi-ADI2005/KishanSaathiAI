from flask import Blueprint, render_template, request, redirect, url_for, session
from services.crop_service import get_crop_prediction
from extensions import csrf
crop_bp = Blueprint("crop", __name__)

# =========================
# SOIL INPUT PAGE
# =========================
@crop_bp.route("/soil")
def soil():
    return render_template("soil.html")


# =========================
# PREDICT ROUTE
# =========================

@crop_bp.route("/predict", methods=["POST"])
@csrf.exempt   
def predict():
    print("FORM DATA:", request.form)  # DEBUG

    try:
        data = request.form

        N = float(data.get("Nitrogen", 0))
        P = float(data.get("Phosphorus", 0))
        K = float(data.get("Potassium", 0))
        temperature = float(data.get("Temperature", 0))
        humidity = float(data.get("Humidity", 0))
        ph = float(data.get("Ph", 0))
        rainfall = float(data.get("Rainfall", 0))

        result = get_crop_prediction(N, P, K, temperature, humidity, ph, rainfall)

        session["crop_result"] = result
        return redirect(url_for("crop.result"))

    except Exception as e:
        print("ERROR:", e)
        session["error"] = str(e)
        return redirect(url_for("crop.soil"))

# =========================
# RESULT PAGE
# =========================
@crop_bp.route("/result")
def result():
    crops = session.get("crop_result")
    error = session.get("error")

    print("RESULT PAGE DATA:", crops)  # ✅ debug

    # ❗ DO NOT clear session before rendering
    return render_template("result.html", crops=crops, error=error)