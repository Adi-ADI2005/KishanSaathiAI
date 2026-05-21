import numpy as np
import joblib

# ✅ MUST BE HERE (GLOBAL)
model = joblib.load("data/model.pkl")
scaler = joblib.load("data/scaler.pkl")

def predict_crop(N, P, K, temperature, humidity, ph, rainfall):
    input_data = [[N, P, K, temperature, humidity, ph, rainfall]]

    scaled_input = scaler.transform(input_data)

    probabilities = model.predict_proba(scaled_input)[0]

    top3_idx = np.argsort(probabilities)[::-1][:3]

    crops = model.classes_

    top3 = [
        {
            "crop": crops[i],
            "confidence": round(probabilities[i] * 100, 2)
        }
        for i in top3_idx
    ]

    return top3