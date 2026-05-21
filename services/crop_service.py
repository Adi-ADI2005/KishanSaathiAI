from ml.predictor import predict_crop

# =========================
# BUSINESS LOGIC LAYER
# =========================
def get_crop_prediction(N, P, K, temperature, humidity, ph, rainfall):
    return predict_crop(N, P, K, temperature, humidity, ph, rainfall)