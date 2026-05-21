import matplotlib
matplotlib.use("Agg")

import cv2
import supervision as sv
import numpy as np
import os
import time
import logging
import gc

logger = logging.getLogger(__name__)

# ==========================================
# GLOBAL MODEL
# ==========================================

model = None


def get_model():

    global model

    if model is None:

        from ultralytics import YOLO

        logger.info("Loading ONNX model...")

        # ✅ Load ONNX model
        model = YOLO("data/best.onnx")

        logger.info("ONNX model loaded successfully")

    return model


# ==========================================
# UPLOAD FOLDER
# ==========================================

UPLOAD_FOLDER = "static/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# DISEASE COLORS
# ==========================================

COLOR_MAP = {
    "Blight": sv.Color(255, 0, 0),
    "Brown Spot": sv.Color(0, 0, 255),
    "False Smut": sv.Color(0, 255, 0),
    "Healthy": sv.Color(255, 255, 0),
    "Leaf Smut": sv.Color(128, 0, 128),
    "Rice blast": sv.Color(255, 165, 0),
    "Stem Rot": sv.Color(255, 0, 255),
    "Tungro": sv.Color(0, 255, 255),
    "Background": sv.Color(255, 255, 255)
}


# ==========================================
# MANAGEMENT GUIDE
# ==========================================

MANAGEMENT_GUIDE = {

    "Blight": {
        "cause": "Fungal infection in rice leaves.",
        "solution": "Apply copper fungicide and avoid excess moisture."
    },

    "Brown Spot": {
        "cause": "Nutrient deficiency and fungal attack.",
        "solution": "Use balanced fertilizer and fungicide."
    },

    "False Smut": {
        "cause": "Fungal disease during flowering stage.",
        "solution": "Use disease-free seeds and spray fungicide."
    },

    "Healthy": {
        "cause": "Plant is healthy.",
        "solution": "Maintain proper irrigation and fertilizer."
    },

    "Leaf Smut": {
        "cause": "Seed-borne fungal disease.",
        "solution": "Treat seeds before sowing."
    },

    "Rice blast": {
        "cause": "Major fungal disease in rice.",
        "solution": "Spray tricyclazole fungicide."
    },

    "Stem Rot": {
        "cause": "Soil-borne fungal infection.",
        "solution": "Improve drainage and apply fungicide."
    },

    "Tungro": {
        "cause": "Virus transmitted by leafhoppers.",
        "solution": "Control insects and remove infected plants."
    }
}


# ==========================================
# NORMALIZE NAMES
# ==========================================

def normalize_name(name):

    return name.strip().lower().replace("_", " ")


# ==========================================
# PROCESS IMAGE
# ==========================================

def process_image(image_path):

    try:

        # ==========================================
        # LOAD MODEL
        # ==========================================

        model = get_model()

        # ==========================================
        # READ IMAGE
        # ==========================================

        image = cv2.imread(image_path)

        if image is None:

            return None, "Image not found", {}, {}

        # ==========================================
        # REDUCE IMAGE SIZE
        # ==========================================

        image = cv2.resize(image, (320, 320))

        # ==========================================
        # PREDICTION
        # ==========================================

        results = model.predict(
            source=image,
            imgsz=320,
            conf=0.4,
            device="cpu",
            verbose=False,
            half=False
        )[0]

        # ==========================================
        # DETECTIONS
        # ==========================================

        detections = sv.Detections.from_ultralytics(results)

        disease_counts = {}

        guidance = {}

        annotated_image = image.copy()

        # ==========================================
        # ANNOTATIONS
        # ==========================================

        if len(detections) > 0:

            box_annotator = sv.BoxAnnotator()

            label_annotator = sv.LabelAnnotator(
                text_color=sv.Color.WHITE,
                text_position=sv.Position.TOP_LEFT
            )

            labels = []

            for idx in range(len(detections)):

                class_id = detections.class_id[idx]

                confidence = detections.confidence[idx]

                class_name = results.names[class_id]

                labels.append(
                    f"{class_name}: {confidence:.2f}"
                )

                # ==========================================
                # COUNT DISEASES
                # ==========================================

                disease_counts[class_name] = (
                    disease_counts.get(class_name, 0) + 1
                )

                # ==========================================
                # MANAGEMENT GUIDE
                # ==========================================

                normalized_name = normalize_name(class_name)

                found = False

                for key in MANAGEMENT_GUIDE:

                    if normalize_name(key) == normalized_name:

                        guidance[class_name] = MANAGEMENT_GUIDE[key]

                        found = True

                        break

                if not found:

                    guidance[class_name] = {
                        "cause": "No data available",
                        "solution": "Consult agriculture expert"
                    }

            # ==========================================
            # DRAW BOXES
            # ==========================================

            annotated_image = box_annotator.annotate(
                scene=annotated_image,
                detections=detections
            )

            # ==========================================
            # DRAW LABELS
            # ==========================================

            annotated_image = label_annotator.annotate(
                scene=annotated_image,
                detections=detections,
                labels=labels
            )

        # ==========================================
        # SUMMARY TEXT
        # ==========================================

        y_offset = 30

        for disease, count in disease_counts.items():

            cv2.putText(
                annotated_image,
                f"{disease}: {count}",
                (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            y_offset += 25

        # ==========================================
        # SAVE OUTPUT IMAGE
        # ==========================================

        timestamp = int(time.time())

        output_filename = f"output_{timestamp}.jpg"

        output_path = os.path.join(
            UPLOAD_FOLDER,
            output_filename
        )

        cv2.imwrite(output_path, annotated_image)

        # ==========================================
        # MEMORY CLEANUP
        # ==========================================

        del image
        del annotated_image
        del results

        gc.collect()

        # ==========================================
        # RETURN RESULT
        # ==========================================

        return (
            f"uploads/{output_filename}",
            None,
            disease_counts,
            guidance
        )

    except Exception as e:

        logger.error(f"Disease Prediction Error: {str(e)}")

        gc.collect()

        return None, str(e), {}, {}